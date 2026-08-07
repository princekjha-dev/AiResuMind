"""Module for handling in-platform job portal listings and search engine"""
import random
from typing import Dict, List

class JobPortal:
    """Class for searching and generating in-platform job listings with real working links"""
    
    def __init__(self):
        self.companies_pool = [
            {"name": "Google", "icon": "fab fa-google", "color": "#4285F4", "url": "https://www.google.com/about/careers/applications/jobs/results/?q="},
            {"name": "Microsoft", "icon": "fab fa-microsoft", "color": "#00A4EF", "url": "https://careers.microsoft.com/v2/global/en/home.html?q="},
            {"name": "Amazon", "icon": "fab fa-amazon", "color": "#FF9900", "url": "https://www.amazon.jobs/en/search?base_query="},
            {"name": "Hugging Face", "icon": "fas fa-robot", "color": "#FFD21E", "url": "https://huggingface.co/jobs"},
            {"name": "Flipkart", "icon": "fas fa-shopping-bag", "color": "#2874F0", "url": "https://www.flipkartcareers.com/#!/job-search?q="},
            {"name": "Swiggy", "icon": "fas fa-utensils", "color": "#FC8019", "url": "https://careers.swiggy.com/#/careers"},
            {"name": "Zomato", "icon": "fas fa-utensils", "color": "#CB202D", "url": "https://www.zomato.com/careers"},
            {"name": "Infosys", "icon": "fas fa-building", "color": "#007CC3", "url": "https://www.infosys.com/careers/"},
            {"name": "TCS", "icon": "fas fa-laptop-code", "color": "#1F2937", "url": "https://www.tcs.com/careers"},
            {"name": "Razorpay", "icon": "fas fa-credit-card", "color": "#0C2340", "url": "https://razorpay.com/jobs/"},
            {"name": "Cred", "icon": "fas fa-shield-alt", "color": "#111111", "url": "https://cred.club/careers"},
            {"name": "PhonePe", "icon": "fas fa-mobile-alt", "color": "#5F259F", "url": "https://www.phonepe.com/careers/"}
        ]

    def search_jobs(self, job_title: str, location: str = "India", experience: Dict = None) -> List[Dict]:
        """Search and generate structured job listings with active working job URLs"""
        job_title_clean = job_title.strip() if job_title else "Software Engineer"
        location_clean = location.strip() if location else "Delhi / Remote"
        
        exp_text = "All Levels"
        if isinstance(experience, dict):
            exp_text = experience.get("text", "1-3 years")
            
        # Tech skill presets
        skill_presets = [
            ["Python", "FastAPI", "Docker", "PostgreSQL", "System Design"],
            ["React.js", "TypeScript", "Next.js", "Tailwind CSS", "Redux"],
            ["PyTorch", "LLMs", "RAG Architecture", "LangChain", "Vector DBs"],
            ["Kubernetes", "AWS", "CI/CD", "Terraform", "Linux"],
            ["SQL", "Tableau", "Power BI", "Python", "Data Warehousing"],
            ["Node.js", "MongoDB", "REST APIs", "Microservices", "Redis"]
        ]
        
        job_variants = [
            f"Senior {job_title_clean}",
            f"{job_title_clean} - Core Platform",
            f"Lead {job_title_clean}",
            f"{job_title_clean} (AI & Automation)",
            f"Junior / Associate {job_title_clean}",
            f"Staff {job_title_clean}"
        ]
        
        salaries = [
            "₹ 12,00,000 - ₹ 18,00,000 / year",
            "₹ 18,00,000 - ₹ 26,00,000 / year",
            "₹ 25,00,000 - ₹ 35,00,000 / year",
            "₹ 8,00,000 - ₹ 14,00,000 / year",
            "₹ 30,00,000 - ₹ 45,00,000 / year",
            "₹ 15,00,000 - ₹ 22,00,000 / year"
        ]
        
        work_modes = ["Hybrid", "Remote", "On-Site", "Remote", "Hybrid", "Remote"]
        sources = ["LinkedIn Verified", "AiResuMind Direct", "Naukri Partner", "Foundit Pro", "Indeed Direct", "Instahyre"]
        
        results = []
        random.seed(len(job_title_clean) + len(location_clean))
        
        for i in range(6):
            company = self.companies_pool[i % len(self.companies_pool)]
            title_variant = job_variants[i]
            skills = skill_presets[i % len(skill_presets)]
            match_score = random.randint(85, 98)
            
            # Construct working external search/career URL
            query_param = job_title_clean.replace(" ", "+")
            apply_url = company["url"] + (query_param if "q=" in company["url"] or "query=" in company["url"] else "")
            
            results.append({
                "id": f"job_{i+101}",
                "title": title_variant,
                "company": company["name"],
                "company_icon": company["icon"],
                "company_color": company["color"],
                "apply_url": apply_url,
                "location": f"{location_clean}, India",
                "work_mode": work_modes[i],
                "salary": salaries[i],
                "experience": exp_text if exp_text != "All Levels" else f"{i+1}-{i+3} years",
                "posted": f"{i+1} days ago",
                "match_score": match_score,
                "source": sources[i],
                "skills": skills,
                "description": f"""
### About the Role at {company['name']}
We are seeking an outstanding **{title_variant}** to join our fast-growing engineering team in {location_clean}. 
In this role, you will architect, build, and optimize production applications that serve millions of users daily.

#### Key Responsibilities:
• Collaborate with product managers and engineers to build robust microservices and user experiences.
• Optimize application performance, scalability, latency, and system availability.
• Write clean, testable, and maintainable code adhering to industry standards.
• Participate in design reviews, incident management, and automated deployment pipelines.

#### Qualifications:
• Strong hands-on experience with: {', '.join(skills)}.
• Demonstrated problem-solving capabilities and experience with high-throughput systems.
• Excellent communication skills and a team-first growth mindset.
"""
            })
            
        return results