import datetime

from pydantic import BaseModel
from typing import List, Optional


class ResponseBase(BaseModel):
    status: str
    message: str


class FlashcardBase(BaseModel):
    question: str
    answer: str
    description: str
    status: int = 0
    level: int = 0
    tags: List[str] = ["default"]


class FlashcardSchema(FlashcardBase):
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class ResponseFlashcardSchema(ResponseBase, FlashcardSchema):
    pass


class ResponseListFlashcardSchema(ResponseBase, BaseModel):
    flashcards: Optional[List[FlashcardSchema]]
