"""
AiResuMind - Telegram Bot Entry Point

Runs independently of the Streamlit app. Start with:
    python telegram_bot.py

Requires:
    - TELEGRAM_BOT_TOKEN in utils/.env
    - OPENROUTER_API_KEY in utils/.env
    - python-telegram-bot >= 20.0

The bot reuses the same extraction and analysis pipeline as the web app.
"""
import os
import sys
import logging
import tempfile
from pathlib import Path

# Make sure the project root is on the path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load env from utils/.env (same location as the web app)
load_dotenv(dotenv_path=Path(__file__).parent / "utils" / ".env")

try:
    from telegram import Update
    from telegram.ext import (
        Application,
        CommandHandler,
        MessageHandler,
        filters,
        ContextTypes,
    )
except ImportError:
    print(
        "python-telegram-bot is not installed.\n"
        "Install it with: pip install python-telegram-bot"
    )
    sys.exit(1)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# In-memory store: last resume text per chat_id (not persisted across restarts)
_last_resume: dict[int, str] = {}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _split_long_message(text: str, limit: int = 4000) -> list[str]:
    """Split a long string into chunks that fit within Telegram's message limit."""
    parts = []
    while len(text) > limit:
        split_at = text.rfind("\n", 0, limit)
        if split_at == -1:
            split_at = limit
        parts.append(text[:split_at])
        text = text[split_at:].lstrip()
    if text:
        parts.append(text)
    return parts


def _extract_text_from_document(file_bytes: bytes, filename: str) -> str:
    """Extract text from PDF or DOCX bytes using the shared AIResumeAnalyzer pipeline."""
    from utils.ai_resume_analyzer import AIResumeAnalyzer
    analyzer = AIResumeAnalyzer()
    fname = (filename or "").lower()
    if fname.endswith(".docx") or fname.endswith(".doc"):
        return analyzer.extract_text_from_docx(file_bytes)
    return analyzer.extract_text_from_pdf(file_bytes)


def _analyze_resume(resume_text: str, job_role: str = "Not specified") -> str:
    """Run the OpenRouter analysis pipeline and return the full text response."""
    from utils.ai_resume_analyzer import AIResumeAnalyzer

    analyzer = AIResumeAnalyzer()
    result = analyzer.analyze_resume_with_openrouter(resume_text, job_role=job_role)
    if not result:
        return "Analysis returned no result. Please try again."
    if "error" in result:
        return f"Analysis error: {result['error']}"
    score = result.get("resume_score", 0)
    ats = result.get("ats_score", 0)
    header = f"Resume Score: {score}/100  |  ATS Score: {ats}/100\n{'=' * 50}\n\n"
    return header + result.get("analysis", "No analysis text returned.")


def _roast_resume(resume_text: str) -> str:
    """Generate a brutal roast of the resume using OpenRouter integration."""
    from utils.ai_resume_analyzer import AIResumeAnalyzer

    analyzer = AIResumeAnalyzer()
    return analyzer.generate_roast(resume_text)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome message explaining the bot."""
    await update.message.reply_text(
        " Welcome to AiResuMind on Telegram!\n\n"
        "This bot provides AI-powered resume analysis, brutal roasts, and interactive Q&A.\n\n"
        " Commands:\n"
        "  /start - Show this welcome message\n"
        "  /jobs [keyword] - Search real-time job listings\n"
        "  /roast - Roast the last resume you sent (brutally honest mode)\n"
        "  /clear - Clear your stored resume from memory\n\n"
        " Interactive Q&A:\n"
        "After sending your PDF or DOCX resume, simply send any question as a text message "
        "(e.g., 'What skills should I add for a Machine Learning role?', 'Summarize my experience', 'How can I rewrite my bullet points?') "
        "and I will answer based on your resume!\n\n"
        "To get started, send your resume as a .pdf or .docx file."
    )


async def cmd_jobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/jobs [keyword] - search real-time job listings directly from Telegram."""
    args = context.args
    keyword = " ".join(args).strip() if args else "Software Engineer"

    await update.message.reply_text(f" Searching for '{keyword}' job opportunities...")
    
    from jobs.suggestions import get_job_suggestions
    results = get_job_suggestions(keyword)
    
    if not results:
        await update.message.reply_text(f"No job listings found for '{keyword}'. Try a query like SDE, AI/ML, or Data Analyst.")
        return
        
    msg_lines = [f" Job Search Results for '{keyword}':\n"]
    for idx, item in enumerate(results[:5], 1):
        msg_lines.append(f"{idx}. {item.get('text', keyword)}")
        
    await update.message.reply_text("\n".join(msg_lines))


async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/clear — remove stored resume for this chat."""
    chat_id = update.effective_chat.id
    if chat_id in _last_resume:
        del _last_resume[chat_id]
        await update.message.reply_text("Your stored resume has been cleared from memory.")
    else:
        await update.message.reply_text("No active resume stored for this chat.")


async def cmd_roast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/roast — run brutal roast on the most recently uploaded resume."""
    chat_id = update.effective_chat.id
    resume_text = _last_resume.get(chat_id)

    if not resume_text:
        await update.message.reply_text(
            "No resume on record for this chat. "
            "Please send a PDF or DOCX resume first, then use /roast."
        )
        return

    await update.message.reply_text("Generating roast. This may take a moment...")
    try:
        roast_text = _roast_resume(resume_text)
    except Exception as exc:
        await update.message.reply_text(f"Roast failed unexpectedly: {str(exc)}")
        return

    header = "--- Brutal Roast ---\n\n"
    for chunk in _split_long_message(header + roast_text):
        await update.message.reply_text(chunk)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle uploaded documents — accept PDF and DOCX, reject everything else."""
    document = update.message.document
    chat_id = update.effective_chat.id

    if not document:
        await update.message.reply_text(
            "Please send a PDF or DOCX file to receive a resume analysis."
        )
        return

    mime = (document.mime_type or "").lower()
    filename = (document.file_name or "").lower()

    is_pdf = filename.endswith(".pdf") or mime == "application/pdf"
    is_docx = filename.endswith(".docx") or filename.endswith(".doc") or "word" in mime or "officedocument" in mime

    if not is_pdf and not is_docx:
        await update.message.reply_text(
            "Only PDF (.pdf) and Word (.docx) resumes are supported. "
            "Please send your resume as a .pdf or .docx file."
        )
        return

    ext = ".docx" if is_docx else ".pdf"
    await update.message.reply_text(
        f"Received your resume ({filename or ext}). Extracting text and running analysis. "
        "This may take up to a minute..."
    )

    # Download the file
    try:
        tg_file = await context.bot.get_file(document.file_id)
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            await tg_file.download_to_drive(tmp.name)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            file_bytes = f.read()
        os.unlink(tmp_path)
    except Exception as exc:
        logger.error("File download failed: %s", exc)
        await update.message.reply_text(
            "Could not download your file. Please try again."
        )
        return

    # Extract text
    try:
        resume_text = _extract_text_from_document(file_bytes, filename)
    except Exception as exc:
        logger.error("Document text extraction failed: %s", exc)
        await update.message.reply_text(
            "Could not extract text from the document. "
            "Make sure the file contains readable text."
        )
        return

    if not resume_text or not resume_text.strip():
        await update.message.reply_text(
            "No readable text found in the document. "
            "Please ensure your resume contains selectable text rather than scanned images."
        )
        return

    # Store for /roast and interactive Q&A
    _last_resume[chat_id] = resume_text

    # Run analysis
    try:
        analysis_text = _analyze_resume(resume_text)
    except Exception as exc:
        logger.error("Analysis failed: %s", exc)
        await update.message.reply_text(
            f"Analysis failed: {str(exc)}. Please try again later."
        )
        return

    # Send result (split if too long)
    for chunk in _split_long_message(analysis_text):
        await update.message.reply_text(chunk)

    await update.message.reply_text(
        " Analysis complete!\n\n"
        " You can now ask me any question about your resume (e.g. 'How can I improve my bullet points?', 'What skills am I missing?'), or use /roast for a brutally honest critique."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages by providing interactive AI Q&A on the stored resume."""
    chat_id = update.effective_chat.id
    user_query = (update.message.text or "").strip()

    if not user_query:
        return

    resume_text = _last_resume.get(chat_id)

    if not resume_text:
        await update.message.reply_text(
            " No resume uploaded yet for this chat!\n\n"
            "Please upload your resume (.pdf or .docx) first. Once uploaded, you can ask me any question about it!"
        )
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    from utils.ai_resume_analyzer import AIResumeAnalyzer
    analyzer = AIResumeAnalyzer()

    prompt = f"""You are an expert AI Career Advisor & Resume Assistant.
The user has uploaded their resume, which is provided below:

--- START RESUME ---
{resume_text}
--- END RESUME ---

User Question: {user_query}

Instructions:
1. Answer the user's question directly, accurately, and constructively based on their resume.
2. If they ask how to improve a section or target a specific role, provide concrete suggestions and examples.
3. Keep the formatting clean and readable for Telegram. Avoid raw Markdown table syntax.
"""

    try:
        answer, _ = analyzer._generate_ai_completion(prompt, temperature=0.7)
    except Exception as exc:
        logger.error("Q&A completion failed: %s", exc)
        answer = f"Sorry, could not answer your question due to an error: {str(exc)}"

    for chunk in _split_long_message(answer):
        await update.message.reply_text(chunk)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print(
            "TELEGRAM_BOT_TOKEN is not set.\n"
            "Add it to utils/.env and try again."
        )
        sys.exit(1)

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("jobs", cmd_jobs))
    app.add_handler(CommandHandler("roast", cmd_roast))
    app.add_handler(CommandHandler("clear", cmd_clear))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("AiResuMind Telegram bot starting (polling)...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
