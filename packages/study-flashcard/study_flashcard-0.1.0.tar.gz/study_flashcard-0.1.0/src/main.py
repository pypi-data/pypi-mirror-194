import requests
from .routes import router as flashcards_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import settings
from mongoengine import connect

connect(db=settings.DB_NAME, host=settings.MONGO_URI, uuidRepresentation='standard')

app = FastAPI()

app.include_router(flashcards_router)
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def homepage(request: Request):
    endpoint = "{base_url}flashcards".format_map({"base_url": request.base_url})
    flashcards = requests.get(endpoint).json()["flashcards"]
    return templates.TemplateResponse("index.html", {"request": request, "flashcards": flashcards})


@app.get("/health")
def read_root():
    return {"ping": "pong"}

