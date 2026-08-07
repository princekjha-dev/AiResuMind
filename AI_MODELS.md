# AI Models in Prince Resume AI

Prince Resume AI uses OpenRouter (with Anthropic Claude 3.5 Sonnet as the default model) to provide detailed, structured analysis and feedback on uploaded resumes.

## Available AI Models

### OpenRouter (Claude 3.5 Sonnet)

OpenRouter acts as a unified API gateway providing access to industry-leading models. By default, Prince Resume AI uses `anthropic/claude-3.5-sonnet`, known for its state-of-the-art natural language processing capabilities. It is used to:

- Analyze resume content and structure
- Identify present and missing skills for a target role
- Provide personalized recommendations for improvement
- Score resumes on quality and relevance (0-100)
- Perform opt-in "Brutal Roast" critiques with actionable fixes

## How AI Analysis Works

1. **Text Extraction** — The system extracts text from your PDF or DOCX resume.
2. **AI Processing** — The OpenRouter client sends the resume text and role information to Claude 3.5 Sonnet.
3. **Structured Output** — The model returns a structured analysis covering:
   - Overall assessment
   - Skills analysis (current and missing)
   - Strengths
   - Areas for improvement
   - Recommended courses
   - Resume score (0-100)
   - ATS optimization assessment (0-100)

## Configuration

Set your OpenRouter API key in `utils/.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get an API key from [OpenRouter](https://openrouter.ai/keys).

## Privacy and Data Handling

- Resume text is sent to OpenRouter for analysis.
- Analysis results are stored locally in the SQLite database.
- No personal data is shared with third parties beyond what is necessary for AI analysis.
- You can delete stored data at any time through the Admin panel.

## Future Integrations

Additional AI models available on OpenRouter may be integrated in future releases by updating the `OPENROUTER_MODEL` configuration constant.