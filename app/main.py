from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routers import auth, consultations, catalogs
from app.core.config import settings
from app.core.exceptions import (
    DomainError,
    DiagnosticNotFound,
    UserNotFound,
    InvalidCredentials,
    EmailRegistered,
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
    return JSONResponse(status_code=http_code, content={"detail": error.message})

def get_http_code(error: DomainError) -> int:
    if isinstance(error, DiagnosticNotFound):
        return 422
    elif isinstance(error, UserNotFound):
        return 404
    elif isinstance(error, InvalidCredentials):
        return 401
    elif isinstance(error, EmailRegistered):
        return 400
    else:
        return 500

@app.exception_handler(Exception)
def manejar_error_inesperado(request: Request, error: Exception):
    print("Error inesperado:", error)
    return JSONResponse(status_code=500, content={"detail": "Ocurrio un error inesperado en el servidor"})


app.include_router(auth.router)
app.include_router(consultations.router)
app.include_router(catalogs.router)

@app.get("/health")
def read_root():
    return {"status": "ok"}
