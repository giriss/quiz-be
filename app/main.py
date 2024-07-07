from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://quiz-fe.gopaul.me",
    "https://quiz-fe.girish.monster",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-token"],
)

app.include_router(router)
