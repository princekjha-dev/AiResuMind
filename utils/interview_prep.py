"""
AI Mock Interview Questions & Prep Generator for AiResuMind
Supports 6 Core Role Options with AI-powered question & strategy generation and candidate answer evaluation.
"""
import json

from utils.ai_resume_analyzer import AIResumeAnalyzer


class InterviewPrepGenerator:
    def __init__(self):
        self.ai_analyzer = AIResumeAnalyzer()
        
        # 6 Core Role Options
        self.available_roles = [
            "Software Engineer (SDE / Full Stack)",
            "AI / Machine Learning Engineer",
            "Data Analyst & BI Specialist",
            "DevOps & Cloud Architect",
            "Product Manager",
            "Cybersecurity Analyst"
        ]
        
        self.question_bank = {
            "Software Engineer (SDE / Full Stack)": [
                {
                    "type": "Technical",
                    "difficulty": "Hard",
                    "question": "How do you optimize a slow database query or bottlenecked API endpoint handling high concurrency?",
                    "answer_guide": "1. **Identify Bottlenecks**: Run APM monitoring (Datadog/NewRelic) and inspect PostgreSQL EXPLAIN ANALYZE plans to spot sequential table scans.\n2. **Database Indexing**: Add composite indices on high-cardinality foreign keys (`user_id`, `created_at`).\n3. **Caching Layer**: Implement a Redis read-aside cache for high-frequency read requests with TTL expiration.\n4. **Connection Pooling**: Configure PgBouncer / HikariCP pool sizing to maintain stable DB connections under high RPS.",
                    "star_framework": {
                        "situation": "Checkout API suffered 1.8s response latency during Black Friday peak traffic.",
                        "task": "Reduce response latency to under 200ms while sustaining 10,000 RPS.",
                        "action": "Diagnosed missing DB indices, implemented Redis payload caching, and refactored synchronous queries to async connection pools.",
                        "result": "Reduced API latency by 88% (to 160ms) and zero downtime at 10k RPS peak."
                    },
                    "keywords": ["Database Indexing", "Redis Caching", "EXPLAIN Plan", "APM Monitoring"]
                },
                {
                    "type": "System Design",
                    "difficulty": "Medium",
                    "question": "How would you design a distributed rate limiter for an API Gateway handling 100,000 requests/sec?",
                    "answer_guide": "1. **Algorithm Selection**: Implement a Sliding Window Counter using Redis Lua scripts for atomic increments.\n2. **Gateway Tier**: Deploy API Gateway instances behind a Network Load Balancer (NLB).\n3. **Distributed Cache**: Utilize a Redis Cluster with read replicas to sustain low-latency key lookups (< 2ms).\n4. **Graceful Fallback**: Fall back to local memory rate limiting if Redis cluster connectivity degrades.",
                    "star_framework": {
                        "situation": "API microservices were vulnerable to malicious scraping and greedy client DDoS spikes.",
                        "task": "Architect a scalable rate limiter enforcing 100 req/min limits across distributed gateways.",
                        "action": "Built an atomic Lua-scripted sliding window rate limiter backed by Redis Cluster.",
                        "result": "Mitigated 100% of DDoS traffic spikes while maintaining 99.99% gateway availability."
                    },
                    "keywords": ["Token Bucket", "Redis Lua Script", "Sliding Window", "API Gateway"]
                },
                {
                    "type": "Behavioral",
                    "difficulty": "Medium",
                    "question": "Describe a critical production outage you managed under tight time constraints.",
                    "answer_guide": "1. **Rapid Triage**: Convened war room, identified faulty deployment, and initiated canary rollback within 3 minutes.\n2. **Stakeholder Communication**: Updated status page and alerted customer support teams.\n3. **Root Cause Analysis (RCA)**: Discovered unhandled NULL exception in authentication microservice payload.\n4. **Preventative Action**: Added mandatory integration test gates to CI/CD pipeline.",
                    "star_framework": {
                        "situation": "A bad deployment broke authentication for 40% of active enterprise users.",
                        "task": "Restore service within 15 minutes and prevent data corruption.",
                        "action": "Initiated immediate automated canary rollback, published status update, and deployed hotfix.",
                        "result": "Full service restored in 8 minutes with zero data loss."
                    },
                    "keywords": ["Incident Management", "Canary Rollback", "RCA Post-Mortem", "Zero Downtime"]
                }
            ],
            "AI / Machine Learning Engineer": [
                {
                    "type": "Technical",
                    "difficulty": "Hard",
                    "question": "How do you handle severe class imbalance and prevent overfitting in deep learning models?",
                    "answer_guide": "1. **Data Resampling**: Apply Synthetic Minority Over-sampling Technique (SMOTE) or Tomek links.\n2. **Loss Function**: Utilize Focal Loss to down-weight easy negative examples and focus on hard minority samples.\n3. **Regularization**: Apply L2 weight decay, dropout layers (0.3-0.5), and early stopping based on validation loss.\n4. **Evaluation**: Measure PR-AUC and F1-score instead of standard accuracy metrics.",
                    "star_framework": {
                        "situation": "Fraud detection dataset contained 99.8% negative and 0.2% positive fraud cases.",
                        "task": "Improve fraud detection recall from 60% to over 90% without increasing false positives.",
                        "action": "Implemented Focal Loss with SMOTE oversampling and tuned classification confidence thresholds.",
                        "result": "Achieved 94% recall rate with a 15% reduction in false positive flags."
                    },
                    "keywords": ["Class Imbalance", "SMOTE", "Focal Loss", "Dropout & Early Stopping"]
                },
                {
                    "type": "System Design",
                    "difficulty": "Hard",
                    "question": "Explain how to architect a production Retrieval-Augmented Generation (RAG) system with low latency vector search.",
                    "answer_guide": "1. **Document Parsing**: Chunk documents semantically with recursive token splitters (500 tokens, 50 overlap).\n2. **Vector Store**: Index embeddings in Qdrant/Pinecone using HNSW (Hierarchical Navigable Small World) indices.\n3. **Hybrid Search**: Combine BM25 keyword search with dense vector similarity via Reciprocal Rank Fusion (RRF).\n4. **Context Compression**: Re-rank retrieved passages using Cohere Rerank before supplying context to LLM.",
                    "star_framework": {
                        "situation": "Enterprise documentation search was slow and produced hallucinated AI responses.",
                        "task": "Architect an accurate RAG pipeline across 500,000 technical PDF documents.",
                        "action": "Built HNSW vector index in Qdrant with hybrid BM25 search and Cohere re-ranking.",
                        "result": "Query latency dropped to 420ms with 96% factual retrieval precision."
                    },
                    "keywords": ["RAG Architecture", "HNSW Vector Search", "Semantic Chunking", "Re-ranking"]
                }
            ],
            "Data Analyst & BI Specialist": [
                {
                    "type": "Technical",
                    "difficulty": "Medium",
                    "question": "What is the order of execution in SQL queries, and how do Window Functions differ from GROUP BY?",
                    "answer_guide": "1. **SQL Execution Order**: `FROM` -> `JOIN` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `WINDOW` -> `ORDER BY` -> `LIMIT`.\n2. **GROUP BY**: Collapses multiple rows into a single summary row per group.\n3. **Window Functions**: Compute aggregations (`SUM() OVER(...)`, `DENSE_RANK()`) across a frame of rows without collapsing underlying record granularity.",
                    "star_framework": {
                        "situation": "Executive leadership required 12-month rolling cohort retention dashboards.",
                        "task": "Build scalable SQL queries driving automated BI dashboards.",
                        "action": "Wrote optimized SQL window queries using `LAG()`, `LEAD()`, and `DENSE_RANK()`.",
                        "result": "Saved 15 analyst hours per week with real-time cohort tracking."
                    },
                    "keywords": ["SQL Execution Order", "Window Functions", "Cohort Analysis", "ETL Optimization"]
                }
            ],
            "DevOps & Cloud Architect": [
                {
                    "type": "Technical",
                    "difficulty": "Hard",
                    "question": "How do you achieve Zero-Downtime deployments on Kubernetes using ArgoCD / Helm?",
                    "answer_guide": "1. **Canary Strategy**: Configure Argo Rollouts to split traffic (10% -> 25% -> 50% -> 100%).\n2. **Service Mesh**: Route traffic dynamically using Istio VirtualServices.\n3. **Health Metrics**: Analyze Prometheus latency and 5xx error rate metrics automatically.\n4. **Automated Rollback**: Trigger instant rollback if error rate exceeds 0.5% threshold.",
                    "star_framework": {
                        "situation": "Monolithic release deployments required 30-minute scheduled maintenance downtime.",
                        "task": "Implement continuous zero-downtime deployments across 50+ microservices.",
                        "action": "Configured Argo Rollouts with Prometheus metric-based canary automated rollbacks.",
                        "result": "Achieved 100% uptime across 120+ seamless production deployments."
                    },
                    "keywords": ["Canary Deployments", "Argo Rollouts", "Service Mesh", "Kubernetes Probes"]
                }
            ],
            "Product Manager": [
                {
                    "type": "Product Sense",
                    "difficulty": "Medium",
                    "question": "How do you prioritize features on a product roadmap when engineering and business stakeholders disagree?",
                    "answer_guide": "1. **Quantifiable Framework**: Score initiatives using RICE (Reach x Impact x Confidence / Effort).\n2. **Stakeholder Tradeoffs**: Map features on Kano model (Must-haves vs. Performance vs. Delighters).\n3. **Data-Driven Alignment**: Present user telemetry and revenue impact models to justify prioritization.",
                    "star_framework": {
                        "situation": "Conflicting feature priorities between sales demands and engineering tech debt.",
                        "task": "Align executives around a unified Q3 product roadmap.",
                        "action": "Scored initiatives using RICE framework and facilitated transparent alignment workshops.",
                        "result": "Achieved 100% executive signoff and increased Q3 feature delivery by 25%."
                    },
                    "keywords": ["RICE Framework", "Roadmap Alignment", "Stakeholder Management", "Kano Model"]
                }
            ],
            "Cybersecurity Analyst": [
                {
                    "type": "Security Technical",
                    "difficulty": "Hard",
                    "question": "How do you investigate and remediate a suspected privilege escalation breach in an AWS cloud infrastructure?",
                    "answer_guide": "1. **Containment**: Revoke compromised IAM session tokens and isolate impacted EC2/EKS instances.\n2. **Investigation**: Query AWS CloudTrail and VPC Flow Logs for unauthorized API calls (`AssumeRole`).\n3. **Remediation**: Update IAM permission boundaries enforcing strict Least Privilege.\n4. **Post-Mortem**: Deploy AWS GuardDuty and Security Hub automated remediation rules.",
                    "star_framework": {
                        "situation": "Unusual IAM role assumption detected outside normal operating hours.",
                        "task": "Contain cloud infrastructure breach and conduct security forensics.",
                        "action": "Isolated impacted VPC, revoked session tokens, and patched misconfigured IAM policy.",
                        "result": "Zero data exfiltration occurred; hardened IAM policies across all environments."
                    },
                    "keywords": ["CloudTrail Logging", "IAM Least Privilege", "Incident Containment", "VPC Security"]
                }
            ]
        }

    def generate_interview_prep(self, job_title="Software Engineer (SDE / Full Stack)", skills=None):
        """Generate AI-powered or structured prep guide based on selected role"""
        skills = skills if skills else []
        role_key = self._match_role(job_title)
        
        # Try AI generation first
        try:
            prompt = f"""
            You are a Senior Principal Engineering Interviewer. Generate 3 highly targeted interview questions for the role: '{role_key}'.
            Candidate Skills: {', '.join(skills) if skills else 'General Technical Skills'}
            
            Return valid JSON list with this EXACT structure:
            [
              {{
                "type": "Technical",
                "difficulty": "Hard",
                "question": "Question text here?",
                "answer_guide": "1. **First Step**: Details here.\\n2. **Second Step**: Details here.\\n3. **Third Step**: Details here.",
                "star_framework": {{
                  "situation": "Clear 1-sentence situation with context.",
                  "task": "Clear 1-sentence task with metric targets.",
                  "action": "Detailed technical actions executed.",
                  "result": "Quantifiable outcome and impact metrics."
                }},
                "keywords": ["Keyword1", "Keyword2", "Keyword3"]
              }}
            ]
            Format 'answer_guide' with markdown numbered steps (1. **Heading**: Description).
            Return ONLY clean JSON without markdown code blocks.
            """
            ai_text, _ = self.ai_analyzer._generate_ai_completion(prompt, temperature=0.6)
            cleaned_json = ai_text.replace("```json", "").replace("```", "").strip()
            parsed_questions = json.loads(cleaned_json)
            if isinstance(parsed_questions, list) and len(parsed_questions) > 0:
                return {
                    "role": role_key,
                    "questions": parsed_questions,
                    "is_ai_generated": True
                }
        except Exception as e:
            print(f"AI Interview Prep fallback used: {e}")

        # Fallback to rich question bank
        questions = self.question_bank.get(role_key, self.question_bank["Software Engineer (SDE / Full Stack)"])
        return {
            "role": role_key,
            "questions": questions,
            "is_ai_generated": False
        }

    def evaluate_user_answer(self, question, user_answer, role, star_framework=None):
        """Evaluate a candidate's practice response with real AI feedback"""
        if not user_answer or len(user_answer.strip()) < 10:
            return {
                "score": 40,
                "feedback": "Please enter a more detailed response to evaluate.",
                "strengths": ["Attempted response"],
                "improvements": ["Provide specific STAR metrics (Situation, Task, Action, Result)."]
            }
        
        try:
            prompt = f"""
            You are a Principal Engineering Interviewer for top tier tech firms. Evaluate the candidate's answer for role '{role}'.
            
            Question: {question}
            Candidate's Answer: {user_answer}
            Target STAR Framework: {json.dumps(star_framework) if star_framework else 'Standard STAR'}
            
            Provide a strict, professional evaluation returned as JSON:
            {{
              "score": 85,
              "feedback": "Detailed 2-3 sentence overall critique.",
              "strengths": ["Strength point 1", "Strength point 2"],
              "improvements": ["Improvement point 1", "Improvement point 2"]
            }}
            Return ONLY clean JSON without codeblocks.
            """
            ai_text, _ = self.ai_analyzer._generate_ai_completion(prompt, temperature=0.5)
            cleaned_json = ai_text.replace("```json", "").replace("```", "").strip()
            res = json.loads(cleaned_json)
            if isinstance(res, dict) and "score" in res:
                return res
        except Exception as e:
            print(f"AI Answer evaluation fallback used: {e}")

        word_count = len(user_answer.split())
        score = min(95, max(50, 50 + (word_count // 3)))
        has_metrics = any(char.isdigit() for char in user_answer)
        
        strengths = ["Structured effort to respond to the prompt."]
        if word_count > 40:
            strengths.append("Detailed context provided in the response.")
        if has_metrics:
            strengths.append("Included quantifiable metrics or numbers.")

        improvements = []
        if not has_metrics:
            improvements.append("Add measurable outcomes and percentage improvements (e.g. reduced latency by 35%).")
        if word_count < 50:
            improvements.append("Elaborate further on the specific Action phase of your STAR response.")

        return {
            "score": score,
            "feedback": f"Solid effort with {word_count} words. Focus on framing your technical achievements with quantifiable impact.",
            "strengths": strengths,
            "improvements": improvements if improvements else ["Refine technical keyword usage."]
        }

    def _match_role(self, job_title):
        """Match title string to one of 6 core options available"""
        title_lower = str(job_title).lower()
        if "ai" in title_lower or "machine learning" in title_lower or "ml" in title_lower:
            return "AI / Machine Learning Engineer"
        elif "analyst" in title_lower or "data" in title_lower or "bi" in title_lower:
            return "Data Analyst & BI Specialist"
        elif "devops" in title_lower or "cloud" in title_lower or "infra" in title_lower:
            return "DevOps & Cloud Architect"
        elif "product" in title_lower or "manager" in title_lower or "pm" in title_lower:
            return "Product Manager"
        elif "cyber" in title_lower or "security" in title_lower or "soc" in title_lower:
            return "Cybersecurity Analyst"
        else:
            return "Software Engineer (SDE / Full Stack)"
