from sqlalchemy.future import select
from backend.models.interaction import Interaction
from datetime import datetime


# 1. LOG
async def log_interaction_tool(data, db):
    try:
        # ✅ SAFE attendees handling
        attendees = data.get("attendees", "")

        # if AI returns list → convert to string
        if isinstance(attendees, list):
            attendees = ", ".join(attendees)

        record = Interaction(
            hcp_name=data.get("hcp_name"),
            interaction_date=datetime.utcnow(),
            attendees=attendees,  # ✅ FIXED (always string)
            topics=data.get("topics", ""),
            sentiment=data.get("sentiment", "Neutral"),
            outcomes=data.get("outcomes", "")
        )

        db.add(record)
        await db.commit()
        await db.refresh(record)

        return record.id

    except Exception as e:
        await db.rollback()
        raise e


# 2. SEARCH
async def search_hcp_tool(name, db):
    result = await db.execute(
        select(Interaction).where(Interaction.hcp_name.ilike(f"%{name}%"))
    )
    return result.scalars().all()


# 3. EDIT
async def edit_interaction_tool(id, data, db):
    result = await db.execute(select(Interaction).where(Interaction.id == id))
    interaction = result.scalar_one_or_none()

    if not interaction:
        return "Not found"

    for key, value in data.items():
        if hasattr(interaction, key) and value is not None:
            setattr(interaction, key, value)

    await db.commit()
    return "Updated"


# 4. DELETE
async def delete_interaction_tool(id, db):
    result = await db.execute(select(Interaction).where(Interaction.id == id))
    interaction = result.scalar_one_or_none()

    if not interaction:
        return "Not found"

    await db.delete(interaction)
    await db.commit()
    return "Deleted"


# 5. SENTIMENT
def validate_sentiment_tool(text):
    text = text.lower()
    if "positive" in text:
        return "Positive"
    if "negative" in text:
        return "Negative"
    return "Neutral"