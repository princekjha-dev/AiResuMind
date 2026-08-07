"""
AI Cover Letter & Candidate Outreach Suite for AiResuMind
Supports Executive Cover Letters, Cold Emails, LinkedIn Connection DMs, Post-based DMs, and Interview Follow-ups.
Multi-provider AI generation (OpenRouter Kimi K3, Groq, Gemini) with fallback engines.
"""
from datetime import datetime

from utils.ai_resume_analyzer import AIResumeAnalyzer


class CoverLetterGenerator:
    def __init__(self):
        self.ai_analyzer = AIResumeAnalyzer()

    def generate_cover_letter(self, name, job_title, company_name, skills, experience_years=3, target_jd="", tone="Professional"):
        """Generate a structured, AI-powered cover letter tailored to the job and company"""
        name = name.strip() if name else "Candidate"
        job_title = job_title.strip() if job_title else "Software Engineer"
        company_name = company_name.strip() if company_name else "Target Company"
        skills_list = skills if isinstance(skills, list) else [s.strip() for s in str(skills).split(",") if s.strip()]
        skills_str = ", ".join(skills_list) if skills_list else "software engineering, problem solving, and system architecture"
        
        try:
            prompt = f"""
            You are an expert executive resume writer and career coach. Write an outstanding, highly tailored cover letter for a candidate.
            
            Candidate Name: {name}
            Target Job Title: {job_title}
            Company Name: {company_name}
            Years of Experience: {experience_years}
            Key Skills: {skills_str}
            Target Job Description / Key Context: {target_jd if target_jd else 'Not specified'}
            Desired Tone: {tone}
            
            Instructions:
            - Write in a {tone.lower()} yet professional tone.
            - Address the Hiring Team at {company_name}.
            - Structure: 
              1. Engaging Opening Paragraph introducing candidate interest.
              2. Core Impact Paragraph connecting skills ({skills_str}) to actual business outcomes and technical achievements.
              3. Alignment Paragraph referencing {company_name}'s goals and the job requirements.
              4. Strong Call to Action and signoff.
            - Do NOT use emojis.
            - Output ONLY the clean cover letter text.
            """
            
            ai_text, _provider = self.ai_analyzer._generate_ai_completion(prompt, temperature=0.7)
            if ai_text and len(ai_text.strip()) > 100:
                return ai_text.strip()
        except Exception as e:
            print(f"AI Cover Letter generation fallback used: {e}")

        date_str = datetime.now().strftime("%B %d, %Y")
        opening = f"Dear Hiring Team at {company_name},"
        
        para1 = (
            f"I am writing to express my enthusiastic interest in the {job_title} position at {company_name}. "
            f"With over {experience_years}+ years of experience in key technical domains including {skills_str}, "
            f"I am confident in my ability to make an immediate impact on your engineering and product goals."
        )

        para2 = (
            f"Throughout my career, I have focused on building scalable, reliable solutions and optimizing performance. "
            f"My expertise aligns closely with the core requirements of {job_title}. I thrive in collaborative, fast-paced environments "
            f"where innovative technology meets practical business impact. Specifically, my proficiency in {skills_str} "
            f"has enabled me to solve complex technical challenges and deliver high-quality deliverables on tight timelines."
        )

        para3 = (
            f"Having reviewed the key objectives outlined in your job description, I am particularly drawn to {company_name}'s "
            f"mission and technical direction. I welcome the opportunity to leverage my background to drive efficiency, "
            f"mentor team members, and contribute directly to upcoming high-priority initiatives."
            if target_jd else
            f"I admire {company_name}'s focus on excellence and technical innovation. I am eager to bring my problem-solving mindset "
            f"and passion for quality software engineering to your team."
        )

        closing = "Thank you for your time and consideration. I look forward to the opportunity to discuss how my background and skills meet your team's needs."
        signoff = f"Sincerely,\n\n{name}"

        return f"{date_str}\n\n{opening}\n\n{para1}\n\n{para2}\n\n{para3}\n\n{closing}\n\n{signoff}"

    def generate_cold_email(self, name, job_title, company_name, recruiter_name="Hiring Manager", skills=None, target_jd="", tone="Executive"):
        """Generate a punchy cold outreach email to recruiters or hiring managers"""
        name = name.strip() if name else "Candidate"
        recruiter = recruiter_name.strip() if recruiter_name else "Hiring Manager"
        job_title = job_title.strip() if job_title else "Software Engineer"
        company = company_name.strip() if company_name else "Company"
        skills_list = skills if isinstance(skills, list) else [s.strip() for s in str(skills).split(",") if s.strip()]
        skills_str = ", ".join(skills_list) if skills_list else "Python, System Design, and Scalable Backend Systems"

        try:
            prompt = f"""
            Write a high-converting Cold Email to a recruiter or hiring manager.
            Candidate Name: {name}
            Recruiter Name: {recruiter}
            Target Job Title: {job_title}
            Company: {company}
            Core Skills: {skills_str}
            Target JD / Context: {target_jd if target_jd else 'High-growth tech role'}
            Tone: {tone}

            Requirements:
            1. Include a captivating Subject Line.
            2. Concise email body (under 175 words).
            3. Highlight 2-3 bullet points showcasing quantifiable achievements and key technical skills ({skills_str}).
            4. Clear, friction-free Call to Action requesting a brief 10-minute intro call.
            5. Do NOT use emojis.
            """
            ai_text, _provider = self.ai_analyzer._generate_ai_completion(prompt, temperature=0.7)
            if ai_text and len(ai_text.strip()) > 80:
                return ai_text.strip()
        except Exception as e:
            print(f"Cold email AI fallback used: {e}")

        top_skill = skills_list[0] if skills_list else "Engineering"
        return f"""Subject: {job_title} Role - {name} ({top_skill} & Scalable Systems)

Hi {recruiter},

I noticed {company} is currently expanding its team for the {job_title} position. Given my background in building high-performance applications with {skills_str}, I wanted to reach out directly.

A quick summary of what I bring to the table:
- Over 3+ years of hands-on experience architecting resilient software solutions.
- Proven track record optimizing backend performance and reducing query latency by up to 40%.
- Core proficiency across {skills_str}.

I would welcome 10 minutes next week to share how my experience aligns with {company}'s technical roadmap. Are you available for a brief call on Tuesday or Thursday afternoon?

Best regards,

{name}
Portfolio/LinkedIn: linkedin.com/in/candidate
"""

    def generate_linkedin_dm(self, name, job_title, company_name, recruiter_name="Hiring Manager", skills=None, tone="Professional"):
        """Generate short LinkedIn connection note (< 300 chars) and InMail outreach"""
        name = name.strip() if name else "Candidate"
        recruiter = recruiter_name.strip() if recruiter_name else "Hiring Manager"
        job_title = job_title.strip() if job_title else "Software Engineer"
        company = company_name.strip() if company_name else "Company"
        skills_list = skills if isinstance(skills, list) else [s.strip() for s in str(skills).split(",") if s.strip()]
        skills_str = ", ".join(skills_list[:3]) if skills_list else "Python, React, System Design"

        try:
            prompt = f"""
            Write TWO LinkedIn outreach messages for candidate {name} targeting recruiter {recruiter} at {company} for role {job_title}:
            Message 1: Short LinkedIn Connection Request Note (MUST BE UNDER 290 CHARACTERS).
            Message 2: Full LinkedIn InMail / Direct Message (under 120 words).
            Key skills: {skills_str}.
            Tone: {tone}.
            Do NOT use emojis.
            """
            ai_text, _provider = self.ai_analyzer._generate_ai_completion(prompt, temperature=0.7)
            if ai_text and len(ai_text.strip()) > 50:
                return ai_text.strip()
        except Exception as e:
            print(f"LinkedIn DM AI fallback used: {e}")

        conn_note = f"Hi {recruiter}, I saw you're hiring for {job_title} at {company}. With expertise in {skills_str}, I'd love to connect and follow your team's work!"
        if len(conn_note) > 290:
            conn_note = f"Hi {recruiter}, interested in the {job_title} role at {company}. I bring experience in {skills_str}. Would love to connect!"

        inmail = f"""Hi {recruiter},

I hope you're having a great week. I've been following {company}'s engineering updates and noticed your opening for {job_title}.

With strong expertise in {skills_str}, I have built production applications delivering real-world technical impact. I'd love to learn more about the team's priority projects and see if my background matches what you're looking for.

Would you be open to a brief chat this week?

Best regards,
{name}"""

        return f"=== OPTION 1: LINKEDIN CONNECTION NOTE (< 300 CHARACTERS) ===\n{conn_note}\n\n=== OPTION 2: LINKEDIN INMAIL / DIRECT MESSAGE ===\n{inmail}"

    def generate_post_based_dm(self, name, job_title, company_name, recruiter_post_snippet="", skills=None, tone="Engaging"):
        """Generate personalized DM responding to a recruiter's hiring post or tweet"""
        name = name.strip() if name else "Candidate"
        job_title = job_title.strip() if job_title else "Software Engineer"
        company = company_name.strip() if company_name else "Company"
        post_snippet = recruiter_post_snippet.strip() if recruiter_post_snippet else f"Looking for a passionate {job_title} to join our tech team!"
        skills_list = skills if isinstance(skills, list) else [s.strip() for s in str(skills).split(",") if s.strip()]
        skills_str = ", ".join(skills_list) if skills_list else "Full Stack & Cloud Systems"

        try:
            prompt = f"""
            Write a personalized LinkedIn/Twitter DM responding directly to a recruiter's post about a job opening.
            Candidate Name: {name}
            Target Role: {job_title}
            Company: {company}
            Recruiter's Post Snippet: "{post_snippet}"
            Candidate Skills: {skills_str}
            Tone: {tone}

            Requirements:
            - Reference the specific post content to show genuine interest.
            - Explain why candidate's experience in {skills_str} fits the post requirements.
            - Keep it conversational, punchy, and under 150 words.
            - Include a quick call to action.
            - Do NOT use emojis.
            """
            ai_text, _provider = self.ai_analyzer._generate_ai_completion(prompt, temperature=0.7)
            if ai_text and len(ai_text.strip()) > 50:
                return ai_text.strip()
        except Exception as e:
            print(f"Post DM AI fallback used: {e}")

        return f"""Hi there,

I just came across your post regarding the {job_title} opening at {company} ("{post_snippet[:80]}..."). 

Your focus on finding someone with hands-on technical execution caught my attention. My background centers on {skills_str}, where I have successfully built and deployed scalable solutions.

I've attached my resume for reference and would love to connect to discuss how I can contribute to this opening.

Best,
{name}"""

    def generate_interview_followup(self, name, job_title, company_name, interviewer_name="Interviewer", key_discussion_point="", tone="Professional"):
        """Generate post-interview thank-you email and follow-up pitch"""
        name = name.strip() if name else "Candidate"
        interviewer = interviewer_name.strip() if interviewer_name else "Interviewer"
        job_title = job_title.strip() if job_title else "Software Engineer"
        company = company_name.strip() if company_name else "Company"
        discussion = key_discussion_point.strip() if key_discussion_point else "our conversation regarding system scalability and team culture"

        try:
            prompt = f"""
            Write a professional post-interview Thank You & Follow-Up email.
            Candidate Name: {name}
            Interviewer Name: {interviewer}
            Target Role: {job_title}
            Company: {company}
            Key Discussion Point to reference: {discussion}
            Tone: {tone}

            Requirements:
            - Express sincere gratitude for the conversation.
            - Reference the key discussion point ({discussion}) to reinforce interest and technical comprehension.
            - Reiterate candidate enthusiasm for {company}.
            - Keep it under 150 words.
            - Do NOT use emojis.
            """
            ai_text, _provider = self.ai_analyzer._generate_ai_completion(prompt, temperature=0.7)
            if ai_text and len(ai_text.strip()) > 50:
                return ai_text.strip()
        except Exception as e:
            print(f"Interview follow-up AI fallback used: {e}")

        return f"""Subject: Thank you - {job_title} Interview ({name})

Hi {interviewer},

Thank you for taking the time to speak with me today about the {job_title} role at {company}.

I really enjoyed learning more about your team's initiatives, particularly {discussion}. That conversation reinforced my enthusiasm for the opportunity and confidence that my technical background is a great fit for {company}'s goals.

Please let me know if you need any additional information or work samples from my end. I look forward to hearing about the next steps.

Best regards,

{name}"""
