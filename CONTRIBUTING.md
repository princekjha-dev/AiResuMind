# Contributing to AiResuMind

Thank you for your interest in contributing to **AiResuMind**! We welcome contributions from developers, designers, and AI researchers.

## Getting Started

1. **Fork the Repository**: Create your own copy of the repository on GitHub.
2. **Clone the Fork**:
   ```bash
   git clone https://github.com/your-username/Smart-AI-Resume-Analyzer.git
   cd Smart-AI-Resume-Analyzer
   ```
3. **Set Up Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Development Guidelines

- **Code Style**: Follow PEP 8 guidelines for Python code.
- **Design Policy**: Maintain the minimal, high-contrast SaaS aesthetic (grayscale/teal palette, clean micro-animations, no unnecessary emojis).
- **Testing**: Ensure all python modules compile cleanly before opening a pull request:
  ```bash
  python3 -m py_compile app.py jobs/job_search.py dashboard/dashboard.py
  ```

## Pull Request Process

1. Create a descriptive feature branch (`git checkout -b feature/amazing-feature`).
2. Commit your changes with clear, concise messages (`git commit -m 'Add ATS keyword recommendation model'`).
3. Push to your branch (`git push origin feature/amazing-feature`).
4. Open a Pull Request against the `main` branch with a clear summary of your changes.

Thank you for contributing!
