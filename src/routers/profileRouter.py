from fastapi import APIRouter , Depends, Form , Request , Response
from src.core.database import get_db 
from src.core.redis_client import get_redis 
from src.services.profileService import create_profile_service , get_profile_service
from src.schema.profileSchema import CreateProfile
from fastapi.templating import Jinja2Templates 
from fastapi.responses import HTMLResponse 
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))

router = APIRouter(prefix="/profile" , tags=["Profile"])

# @router.post("/", response_class=HTMLResponse)
# async def create_profile(
#     request: Request,
#     data: CreateProfile,
#     db: AsyncSession = Depends(get_db),
#     redis: Redis = Depends(get_redis),
# ):
#     profile = await create_profile_service(
#         db=db,
#         data=data,
#         username=data.username,
#         redis=redis,
#     )

#     return templates.TemplateResponse(
#         "create.html",
#         {
#             "request": request,
#             "profile": profile,
#         },
#     )

@router.get("/", response_class=HTMLResponse)
async def create_profile_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={}
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
        name="create.html",
        context={}
    )


@router.get("/{username}" , response_class=HTMLResponse)
async def get_profile(
    request: Request,
    username : str ,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    profile = await get_profile_service(
        db = db , 
        redis= redis ,
        username= username
    )

    return templates.TemplateResponse(
        request=request,
        name="username.html",
        context={"profile": profile}
    )