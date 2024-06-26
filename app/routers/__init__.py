from fastapi import APIRouter
from .account import router as accounts_router
from .email import router as emails_router

router = APIRouter()
accounts_router.include_router(emails_router, prefix="/emails")
router.include_router(accounts_router, prefix="/accounts")
