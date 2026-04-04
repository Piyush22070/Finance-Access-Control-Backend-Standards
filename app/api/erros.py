from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
import traceback

async def sqlalchemy_integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=400, content={"detail": "Database conflict."})

async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"detail": "Server error."})