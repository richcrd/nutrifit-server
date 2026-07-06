from fastapi import FastAPI

app = FastAPI(title="Nutri Fit")

@app.get("/health")
def read_root():
    return {"status": "ok"}
