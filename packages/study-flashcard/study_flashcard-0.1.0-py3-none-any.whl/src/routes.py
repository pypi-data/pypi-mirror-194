import datetime

from fastapi import APIRouter
from .models import Flashcard
from .schemas import FlashcardSchema, ResponseFlashcardSchema, ResponseListFlashcardSchema


router = APIRouter()


@router.get("/flashcards", response_model=ResponseListFlashcardSchema)
def get_flashcards():
    objs = Flashcard.objects().all()
    if objs:
        rs = {
            "status": "success",
            "message": "Get all flashcards",
            "flashcards": [FlashcardSchema(**obj.to_mongo().to_dict()) for obj in objs]
        }
    else:
        rs = {
            "status": "success",
            "message": "flashcards are empty",
            "flashcards": []
        }

    return rs


@router.post("/flashcards", response_model=ResponseFlashcardSchema)
def create_flashcard(flashcard: FlashcardSchema):
    flashcard_obj = Flashcard.objects(question=flashcard.question).first()
    if not flashcard_obj:
        flashcard_obj = Flashcard(
            question=flashcard.question,
            answer=flashcard.answer,
            description=flashcard.description,
            status=flashcard.status,
            level=flashcard.level,
            created_at=datetime.datetime.utcnow()
        )
        flashcard_obj.save()
        rs = {
            "status": "success",
            "message": "create new a flashcard"
        }
    else:
        Flashcard.objects(question=flashcard.question).update_one(
            set__answer=flashcard.answer,
            set__description=flashcard.description,
            set__level=flashcard.level,
            set__status=flashcard.status
        )
        rs = {
            "status": "success",
            "message": "update flashcard"
        }
    obj = Flashcard.objects(question=flashcard.question).first()
    rs.update(obj.to_mongo().to_dict())
    return ResponseFlashcardSchema(**rs)
