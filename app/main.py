from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routers import auth, consultations, catalogs
from app.api.response import success_response
from app.core.config import settings
from app.core.exceptions import (
    DomainError,
    DiagnosticNotFound,
    UserNotFound,
    InvalidCredentials,
    EmailRegistered,
    InvalidRefreshToken,
)

app = FastAPI(title="Nutri Fit")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(DomainError)
def handle_domain_error(request: Request, error: DomainError):
    http_code = get_http_code(error)
    return JSONResponse(
        status_code=http_code,
        content={"code": http_code, "message": error.message, "response": None},
    )

@app.exception_handler(StarletteHTTPException)
def handle_http_exception(request: Request, error: StarletteHTTPException):
    return JSONResponse(
        status_code=error.status_code,
        content={"code": error.status_code, "message": str(error.detail), "response": None},
    )

def get_http_code(error: DomainError) -> int:
    if isinstance(error, DiagnosticNotFound):
        return 422
    elif isinstance(error, UserNotFound):
        return 404
    elif isinstance(error, InvalidCredentials):
        return 401
    elif isinstance(error, EmailRegistered):
        return 400
    elif isinstance(error, InvalidRefreshToken):
        return 401
    else:
        return 500

@app.exception_handler(Exception)
def manejar_error_inesperado(request: Request, error: Exception):
    print("Error inesperado:", error)
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": "Ocurrio un error inesperado en el servidor", "response": None},
    )


app.include_router(auth.router)
app.include_router(consultations.router)
app.include_router(catalogs.router)

@app.get("/health")
def read_root():
    return success_response(data={"status": "ok"}, message="Servidor operativo")
