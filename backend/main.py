from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔥 IMPORT BOTH ROUTERS
from backend.routers import chat_routes, interaction_routes

from backend.core.database import engine, Base

app = FastAPI(title="AI CRM Backend")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTERS (VERY IMPORTANT)
app.include_router(chat_routes.router, prefix="/chat", tags=["Chat"])
app.include_router(interaction_routes.router, prefix="/interaction", tags=["Interaction"])

# ✅ CREATE TABLES
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ✅ ROOT CHECK
@app.get("/")
def home():
    return {"status": "running"}