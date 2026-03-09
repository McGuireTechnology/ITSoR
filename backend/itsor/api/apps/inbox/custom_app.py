from fastapi import FastAPI

app = FastAPI(
    title="ITSoR : Custom API",
    description="Custom sub-application",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
