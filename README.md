 🚀 AI-First CRM HCP Module – Log Interaction Screen

📌 Overview
This project is an **AI-powered CRM (Customer Relationship Management) module** designed for logging and managing interactions with Healthcare Professionals (HCPs).

It allows users to:
- Log interactions via a **structured form**
- Log interactions via an **AI-powered chat interface**

The system uses **LangGraph + LLM (Groq)** to extract structured data from natural language.

 🧠 Key Features

 ✅ Log Interaction
- Manual form entry
- AI chat-based logging using natural language

 ✅ AI Extraction
Automatically extracts:
- HCP Name
- Date & Time
- Attendees
- Topics Discussed
- Sentiment (Positive / Neutral / Negative)
- Outcomes

✅ Search Interaction
- Search interactions by HCP name
- Results displayed in UI (no alerts)

✅ Edit Interaction
- Modify existing interaction details

✅ Delete Interaction
- Remove interaction records

✅ Sentiment Analysis
- Automatic sentiment detection using AI tools


🏗️ Tech Stack

# Frontend
- React.js
- Redux Toolkit
- CSS (Google Inter font)

# Backend
- FastAPI (Python)
- SQLAlchemy (Async)

# AI Layer
- LangGraph
- Groq LLM (gemma2-9b-it / llama-3.1)

# Database
- MySQL

 🔗 System Architecture


User (Form / Chat)
↓
React + Redux (Frontend)
↓
FastAPI Backend
↓
LangGraph Agent
↓
Tools (Log, Search, Edit, Delete, Sentiment)
↓
MySQL Database


🤖 LangGraph Agent & Tools

The LangGraph agent acts as the **decision-making engine**.

 🔧 Tools Implemented:

1. **Log Interaction Tool**
   - Uses LLM to extract structured data
   - Saves interaction into database

2. **Search HCP Tool**
   - Retrieves interactions by doctor name

3. **Edit Interaction Tool**
   - Updates existing records

4. **Delete Interaction Tool**
   - Deletes records from database

5. **Sentiment Analysis Tool**
   - Determines sentiment from input text


 ▶️ How to Run the Project

🔹 Backend (FastAPI)

bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
🔹 Frontend (React)
cd frontend
npm install
npm start
📸 Demo Flow
Enter interaction manually → Save → View in list

Use AI chat:

Met Dr Sneha Joshi yesterday at 2 PM with nurse Ravi discussed insulin therapy positive
AI auto-fills the form
Submit → Data saved
Search → Results displayed in UI
🧪 Sample Inputs
Met Dr Rajesh Patel at 3 PM discussed diabetes treatment positive
Search Dr Sneha Joshi
Delete interaction 5
Edit interaction 3



📊 Outcome

This project demonstrates:

AI-first application design
Natural language to structured data conversion
Full-stack integration (React + FastAPI + AI)
Real-time data handling with database
🎯 Key Learnings
Working with LangGraph agents
Integrating LLM with backend systems
Building scalable APIs using FastAPI
State management using Redux
📌 Future Improvements
Better UI/UX (cards, filters, pagination)
Advanced NLP for improved extraction
Role-based authentication
Deployment (Netlify + Render/AWS)


👨‍💻 Author

Himanshu Gadekar
B.Tech CSE | Full Stack + AI/ML Developer
