import datetime

from mongoengine import Document, IntField, StringField, ListField, DateTimeField, ReferenceField


class Flashcard(Document):
    question = StringField(required=True, unique=True)
    answer = StringField(required=True)
    description = StringField(required=True, default="")
    status = IntField(required=True, default=0)
    level = IntField(required=True, default=0)
    tags = ListField(StringField(required=True), default=["default"])
    created_at = DateTimeField(required=False)
    updated_at = DateTimeField(required=False, default=datetime.datetime.utcnow)
