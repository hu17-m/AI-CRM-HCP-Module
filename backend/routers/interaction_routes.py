from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.future import select

from backend.core.database import get_db
from backend.schemas.interaction_schema import InteractionCreate
from backend.services.interaction_service import create_interaction
from backend.models.interaction import Interaction

router = APIRouter()


# ✅ CREATE
@router.post("/")
async def create(data: InteractionCreate, db=Depends(get_db)):
    try:
        result = await create_interaction(db, data)

        return {
            "status": "success",
            "data": {
                "id": result.id,
                "hcp_name": result.hcp_name,
                "interaction_date": str(result.interaction_date),
                "topics": result.topics,
                "sentiment": result.sentiment,
                "outcomes": result.outcomes
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET ALL
@router.get("/all")
async def get_all(db=Depends(get_db)):
    result = await db.execute(select(Interaction))
    interactions = result.scalars().all()

    return [
        {
            "id": i.id,
            "hcp_name": i.hcp_name,
            "interaction_date": str(i.interaction_date),
            "topics": i.topics,
            "sentiment": i.sentiment,
            "outcomes": i.outcomes
        }
        for i in interactions
    ]


# ✅ SEARCH
@router.get("/search")
async def search(name: str = Query(...), db=Depends(get_db)):
    result = await db.execute(
        select(Interaction).where(Interaction.hcp_name.ilike(f"%{name}%"))
    )
    data = result.scalars().all()

    return [
        {
            "id": i.id,
            "hcp_name": i.hcp_name,
            "interaction_date": str(i.interaction_date),
            "topics": i.topics,
            "sentiment": i.sentiment,
            "outcomes": i.outcomes
        }
        for i in data
    ]


# ✅ UPDATE
@router.put("/update/{id}")
async def update(id: int, updated_data: dict, db=Depends(get_db)):
    result = await db.execute(select(Interaction).where(Interaction.id == id))
    interaction = result.scalar_one_or_none()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    for key, value in updated_data.items():
        if hasattr(interaction, key):
            setattr(interaction, key, value)

    await db.commit()
    await db.refresh(interaction)

    return {"status": "success", "message": "Updated successfully"}


# ✅ DELETE
@router.delete("/delete/{id}")
async def delete(id: int, db=Depends(get_db)):
    result = await db.execute(select(Interaction).where(Interaction.id == id))
    interaction = result.scalar_one_or_none()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    await db.delete(interaction)
    await db.commit()

    return {"status": "success", "message": "Deleted successfully"}