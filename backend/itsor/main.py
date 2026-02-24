from contextlib import asynccontextmanager

from fastapi import FastAPI

from itsor.infrastructure.container.database import create_tables
from itsor.api.routes.auth import router as auth_router
from itsor.api.routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="ITSoR API",
    description="IT System of Record API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def read_root():
    return {"message": "ITSoR API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
