from fastapi import APIRouter, Depends
from backend.agents.langgraph_agent import app_graph
from backend.core.database import get_db
from backend.schemas.chat_schema import ChatRequest

router = APIRouter()

@router.post("/chat")
async def chat(body: ChatRequest, db=Depends(get_db)):
    try:
        state = {
            "user_query": body.query,
            "db": db
        }

        result = await app_graph.ainvoke(state)

        # 🔥 always return safe structure
        return {
            "action": result.get("action", "error"),
            "message": result.get("message", ""),
            "extracted_data": result.get("extracted_data", {}),
            "data": result.get("data", [])
        }

    except Exception as e:
        return {
            "action": "error",
            "message": str(e),
            "extracted_data": {}
        }