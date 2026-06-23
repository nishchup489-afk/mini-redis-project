from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.core.database import get_db
from src.core.redis_client import get_redis

from src.services.profileService import (
    create_profile_service,
    get_profile_service,
    update_profile_service,
    delete_profile as delete_profile_service,
    get_all_profile_service
)

from src.schema.profileSchema import CreateProfile, UpdateProfile


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_class=HTMLResponse)
async def create_profile_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={},
    )


@router.get("/all" , response_class=HTMLResponse)
async def profile_feed(
    request : Request , 
    db : AsyncSession = Depends(get_db) , 
    redis : Redis = Depends(get_redis)
):
    profiles = await get_all_profile_service(
        db=db , 
        redis=redis
    )

    return templates.TemplateResponse(
        request=request , 
        name="index.html",
        context={"profiles" : profiles}
    )


@router.post("/", response_class=HTMLResponse)
async def create_profile(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    github: str = Form(...),
    email: str = Form(...),
    linkedin: str = Form(...),
    portfolio: str | None = Form(None),
    X: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    data = CreateProfile(
        first_name=first_name,
        last_name=last_name,
        username=username,
        github=github,
        email=email,
        linkedin=linkedin,
        portfolio=portfolio,
        X=X,
    )

    profile = await create_profile_service(
        db=db,
        data=data,
        username=data.username,
        redis=redis,
    )

    return templates.TemplateResponse(
        request=request,
        name="username.html",
        context={"profile": profile},
    )


@router.get("/{username}", response_class=HTMLResponse)
async def get_profile(
    request: Request,
    username: str,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    profile = await get_profile_service(
        db=db,
        redis=redis,
        username=username,
    )

    return templates.TemplateResponse(
        request=request,
        name="username.html",
        context={"profile": profile},
    )


@router.get("/{username}/update", response_class=HTMLResponse)
async def get_update_user_page(
    request: Request,
    username: str,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    profile = await get_profile_service(
        db=db,
        redis=redis,
        username=username,
    )

    return templates.TemplateResponse(
        request=request,
        name="update.html",
        context={"profile": profile},
    )


@router.post("/{old_username}/update", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    old_username: str,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    github: str = Form(...),
    email: str = Form(...),
    linkedin: str = Form(...),
    portfolio: str | None = Form(None),
    X: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    data = UpdateProfile(
        first_name=first_name,
        last_name=last_name,
        username=username,
        github=github,
        email=email,
        linkedin=linkedin,
        portfolio=portfolio,
        x=X,
    )

    profile = await update_profile_service(
        db=db,
        redis=redis,
        username=old_username,
        data=data,
    )

    return templates.TemplateResponse(
        request=request,
        name="username.html",
        context={"profile": profile},
    )


@router.post("/{username}/delete", response_class=HTMLResponse)
async def delete_profile(
    request: Request,
    username: str,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    await delete_profile_service(
        db=db,
        username=username,
        redis=redis,
    )

    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={"message": "Profile deleted successfully"},
    )


