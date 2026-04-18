from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from backend.core.config import settings
from backend.agents.tools import (
    validate_sentiment_tool,
    log_interaction_tool,
    search_hcp_tool,
    edit_interaction_tool,
    delete_interaction_tool
)

import json, re
from datetime import datetime

llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)


# -----------------------------
# 🔥 MAIN AGENT NODE
# -----------------------------
async def agent_node(state: dict):
    query = state.get("user_query", "").strip()
    query_lower = query.lower()
    db = state.get("db")

    try:
        # -----------------------------
        # 🧠 INTENT DETECTION
        # -----------------------------
        if query_lower.startswith("search") or query_lower.startswith("find") or query_lower.startswith("show"):
            action = "search"

        elif any(word in query_lower for word in ["delete", "remove"]):
            action = "delete"

        elif any(word in query_lower for word in ["edit", "update", "change"]):
            action = "edit"

        else:
            action = "log"

        # -----------------------------
        # 🔍 SEARCH TOOL
        # -----------------------------
        if action == "search":
            match = re.search(r"dr\.?\s+[a-z]+", query_lower)
            name = match.group() if match else query_lower

            results = await search_hcp_tool(name, db)

            return {
                "action": "search",
                "message": "Search results",
                "data": [
                    {
                        "hcp_name": r.hcp_name,
                        "topics": r.topics,
                        "sentiment": r.sentiment
                    }
                    for r in results
                ]
            }

        # -----------------------------
        # ❌ DELETE TOOL
        # -----------------------------
        if action == "delete":
            words = query_lower.split()
            interaction_id = next((int(w) for w in words if w.isdigit()), None)

            if not interaction_id:
                return {"action": "error", "message": "Interaction ID required"}

            msg = await delete_interaction_tool(interaction_id, db)

            return {
                "action": "delete",
                "message": msg
            }

        # -----------------------------
        # ✏️ EDIT TOOL
        # -----------------------------
        if action == "edit":
            words = query_lower.split()
            interaction_id = next((int(w) for w in words if w.isdigit()), None)

            if not interaction_id:
                return {"action": "error", "message": "Interaction ID required"}

            updated_data = {"topics": "Updated via AI"}

            msg = await edit_interaction_tool(interaction_id, updated_data, db)

            return {
                "action": "edit",
                "message": msg
            }

        # -----------------------------
        # 🧠 LOG TOOL (LLM EXTRACTION)
        # -----------------------------
        prompt = f"""
Extract structured JSON from the text.

Rules:
- Convert time like "11:30 AM" → "11:30"
- Convert "today", "yesterday", "tomorrow" into YYYY-MM-DD
- If date not given → use today's date
- If time not given → keep empty ""
- Extract clean doctor name (hcp_name)
- Extract attendees (people mentioned after 'with', 'along with', 'accompanied by')
- Extract only meaningful topics

Return ONLY valid JSON.
No explanation.
No markdown.

Keys:
hcp_name, date, time, attendees, topics, sentiment, outcomes

Text:
{query}
"""

        response = await llm.ainvoke(prompt)

        clean = re.sub(r"```json|```", "", response.content).strip()

        try:
            extracted = json.loads(clean)
        except Exception:
            print("❌ JSON ERROR:", clean)
            extracted = {}

        # ✅ FIXED (list → string conversion for ALL fields)
        attendees_val = extracted.get("attendees", "")
        topics_val = extracted.get("topics", "")
        outcomes_val = extracted.get("outcomes", "")

        if isinstance(attendees_val, list):
            attendees_val = ", ".join(attendees_val)

        if isinstance(topics_val, list):
            topics_val = ", ".join(topics_val)

        if isinstance(outcomes_val, list):
            outcomes_val = ", ".join(outcomes_val)

        # ✅ NEW: fallback if AI misses attendees
        if not attendees_val:
            match = re.search(r"(with|along with|accompanied by)\s+([a-zA-Z\s]+)", query_lower)
            if match:
                attendees_val = match.group(2).strip()

        extracted = {
            "hcp_name": extracted.get("hcp_name", ""),
            "date": extracted.get("date", datetime.now().strftime("%Y-%m-%d")),
            "time": extracted.get("time", ""),
            "attendees": attendees_val,
            "topics": topics_val,
            "sentiment": validate_sentiment_tool(query),
            "outcomes": outcomes_val
        }

        # ❌ prevent bad logs
        if not extracted["hcp_name"] or not extracted["topics"]:
            return {
                "action": "error",
                "message": "AI could not extract proper data",
                "extracted_data": {}
            }

        # -----------------------------
        # 💾 SAVE
        # -----------------------------
        interaction_id = await log_interaction_tool(extracted, db)

        return {
            "action": "log",
            "message": "Saved successfully",
            "interaction_id": interaction_id,
            "extracted_data": extracted
        }

    except Exception as e:
        return {
            "action": "error",
            "message": str(e),
            "extracted_data": {}
        }


# -----------------------------
# 🔗 GRAPH SETUP
# -----------------------------
workflow = StateGraph(dict)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")

app_graph = workflow.compile()