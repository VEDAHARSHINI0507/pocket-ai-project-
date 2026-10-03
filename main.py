from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import APP_NAME, SECRET_KEY
from app.database import Base, engine
from app.routes import auth, pages, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    debug=True
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(recommendations.router)