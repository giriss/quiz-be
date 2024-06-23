from fastapi import APIRouter
from .account import router as accounts_router

router = APIRouter()

router.include_router(accounts_router, prefix="/accounts")
