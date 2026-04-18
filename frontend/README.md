🚀 AI-First CRM HCP Module – Log Interaction Screen

📌 Overview
This project is an **AI-powered CRM module** designed for logging and managing interactions with Healthcare Professionals (HCPs).  
It allows users to log interactions using both:
- 📋 Structured Form
- 💬 AI Chat Interface (LangGraph + LLM)

The system automatically extracts key details like **doctor name, date, time, attendees, topics, and sentiment** using AI.


🧠 Key Features

✅ 1. Log Interaction
- Manual form-based entry
- AI-powered chat logging using natural language

✅ 2. AI Data Extraction
- Extracts:
  - HCP Name
  - Date & Time
  - Attendees
  - Topics
  - Sentiment
  - Outcomes

✅ 3. Search Interaction
- Search interactions by doctor name
- Results displayed directly in UI

✅ 4. Edit Interaction
- Modify existing interaction details

✅ 5. Delete Interaction
- Remove unwanted records

✅ 6. Sentiment Analysis
- Automatically detects:
  - Positive
  - Neutral
  - Negative


🏗️ Tech Stack

# Frontend
- React.js
- Redux Toolkit
- CSS

# Backend
- FastAPI (Python)
- SQLAlchemy (Async)

# AI Layer
- LangGraph
- Groq LLM API

# Database
- MySQL


🔗 System Architecture


User (Form / Chat)
↓
React Frontend (Redux)
↓
FastAPI Backend
↓
LangGraph Agent
↓
Tools (Log, Search, Edit, Delete, Sentiment)
↓
MySQL Database



🤖 LangGraph Agent & Tools

The LangGraph agent acts as the **central brain** of the system.

🔧 Tools Implemented:

1. **Log Interaction Tool**
   - Extracts structured data using LLM
   - Saves interaction into database

2. **Search HCP Tool**
   - Retrieves interactions by doctor name

3. **Edit Interaction Tool**
   - Updates interaction fields

4. **Delete Interaction Tool**
   - Removes interaction from database

5. **Sentiment Analysis Tool**
   - Detects sentiment from text input


▶️ How to Run
 🔹 Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
🔹 Frontend (React)
cd frontend
npm install
npm start
📸 Demo Flow
Enter interaction via form → Save → View in list

Enter natural language in chat:

Met Dr Sneha Joshi yesterday at 2 PM with nurse Ravi discussed insulin therapy positive
AI auto-fills form
Search doctor → Results shown in UI
🧪 Sample Inputs
Met Dr Rajesh Patel at 3 PM discussed diabetes treatment positive
Search Dr Sneha Joshi
Delete interaction 5
Edit interaction 3
📊 Outcome

This project demonstrates:

AI-first workflow design
Real-time data extraction using LLM
Integration of LangGraph agent with backend
Full-stack CRM system with modern UI
🎯 Key Learnings
Building AI-driven applications using LangGraph
Integrating LLM with structured databases
Designing scalable backend APIs
Managing state using Redux
📌 Future Improvements
Better UI for edit/delete actions
Pagination & filtering
Advanced NLP for better extraction
Role-based access control
👨‍💻 Author

Himanshu Gadekar
B.Tech CSE | Full Stack + AI/ML Developer