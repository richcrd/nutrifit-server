from fastapi import FastAPI
from app.api.routers import auth, consultations, catalogs

app = FastAPI(title="Nutri Fit")

app.include_router(auth.router)
app.include_router(consultations.router)
app.include_router(catalogs.router)

@app.get("/health")
def read_root():
    return {"status": "ok"}
