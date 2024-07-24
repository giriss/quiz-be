from fastapi import APIRouter
from .account import router as accounts_router
from .email import router as emails_router
from .connection import router as connection_router

router = APIRouter()
accounts_router.include_router(emails_router, prefix="/emails")
accounts_router.include_router(connection_router, prefix="/connections")
router.include_router(accounts_router, prefix="/accounts")
