from typing import Dict, Optional

from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from app.schema import Feedback, FeedbackUpdate, FeedbackOptions
from app.schema import Mentor, MentorUpdate, Mentee, MenteeUpdate
from app.sentiment import sentiment_rank

Router = APIRouter(
    prefix="/data",
    tags=["Data Operations"]
)

@Router.post("/create/feedback")
async def create_feedback(data: Feedback):
    data_dict = data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": Router.db.create("Feedback", data_dict)}

@Router.post("/read/feedback")
async def read_feedback(query: FeedbackOptions):
    return {"result": Router.db.read("Feedback", query.dict(exclude_none=True))}

@Router.patch("/update/feedback")
async def update_feedback(ticket_id: str, update_data: FeedbackUpdate):
    data_dict = update_data.dict(exclude_none=True)
    data_dict["vader_score"] = sentiment_rank(data_dict["text"])
    return {"result": Router.db.update("Feedback", {"ticket_id": ticket_id}, data_dict)}

@Router.delete("/delete/feedback")
async def delete_feedback(ticket_id: str):
    Router.db.delete("Feedback", {"ticket_id": ticket_id})
    return {"result": {"deleted": ticket_id}}