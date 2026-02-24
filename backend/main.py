from fastapi import FastAPI

app = FastAPI(title="ITSoR API", description="IT System of Record API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "ITSoR API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
