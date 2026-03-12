from fastapi import FastAPI

from itsor.api.routes.itam import reports_router

app = FastAPI(
    title="ITSoR : ITAM API",
    description="IT Asset Management sub-application",
    version="0.1.0",
)

app.include_router(reports_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
