from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.interaction import Interaction


# ---------------- CREATE ----------------
async def create_interaction(db: AsyncSession, data):
    try:
        # ✅ SAFE dict extraction
        payload = data.dict() if hasattr(data, "dict") else data

        interaction = Interaction(**payload)

        db.add(interaction)
        await db.commit()
        await db.refresh(interaction)

        return interaction

    except Exception as e:
        await db.rollback()
        raise e


# ---------------- GET BY HCP ----------------
async def get_interactions_by_hcp(db: AsyncSession, name: str):
    result = await db.execute(
        select(Interaction).where(Interaction.hcp_name == name)
    )
    return result.scalars().all()


# ---------------- UPDATE ----------------
async def update_interaction(db: AsyncSession, id: int, data: dict):
    interaction = await db.get(Interaction, id)

    if not interaction:
        raise Exception("Interaction not found")

    for key, value in data.items():
        if hasattr(interaction, key) and value is not None:
            setattr(interaction, key, value)

    await db.commit()
    await db.refresh(interaction)

    return interaction


# ---------------- DELETE ----------------
async def delete_interaction(db: AsyncSession, id: int):
    interaction = await db.get(Interaction, id)

    if not interaction:
        raise Exception("Interaction not found")

    await db.delete(interaction)
    await db.commit()

    return {"message": "Deleted successfully"}