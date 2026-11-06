GenAI Smart Assistant – Week 5

Project Overview

GenAI Smart Assistant is an AI-powered application developed using Python, Gemini API, and Streamlit.

It uses AI agent function calling to select and execute Python tools based on user requests.

Features

- Live weather information using a public weather API.
- Loan EMI calculation using a mathematical formula.
- Gemini function calling.
- Agentic loop for executing Python tools.
- Streamlit chat interface.
- Conversation history.
- Tool-use status indicators.

Technologies Used

- Python
- Google Gemini API
- Streamlit
- Open-Meteo Weather API
- Python-dotenv

Project Structure

GenAI-Week5-Smart-Assistant/
│
├── app.py
├── agent.py
├── tools.py
├── requirements.txt
├── troubleshooting_log.md
├── README.md
└── .gitignore

Installation

Install dependencies:

pip install -r requirements.txt

Create a ".env" file and add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

Run the Application

python -m streamlit run app.py

Testing

The application was tested with:

1. Weather information for Mardan.
2. EMI calculation for Rs. 800,000 at 15% annual interest for 36 months.
3. Normal conversational questions.

Internship

GenAI Engineering Internship – Week 5
Uzair AI Studio
