from fastapi import FastAPI 
from contextlib import asynccontextmanager
from src.models.profile import Profile 
from src.routers.profileRouter import router
from src.core.redis_client import init_redis , close_redis
from src.core.database import engine , Base
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse 
from fastapi import Request , Response

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)
@asynccontextmanager
async def lifespan(app : FastAPI):
    await init_redis()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await close_redis()
    await engine.dispose()
    

app = FastAPI(lifespan=lifespan)



app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )