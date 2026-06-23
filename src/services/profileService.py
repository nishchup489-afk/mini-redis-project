from src.models.profile import Profile 
from src.schema.profileSchema import CreateProfile , GetProfile , UpdateProfile 
from src.core.redis_client import get_redis 
from sqlalchemy import select , update
from sqlalchemy.ext.asyncio import AsyncSession 
from redis.asyncio import Redis 
from fastapi.templating import Jinja2Templates
from pathlib import Path 
from fastapi import HTTPException
import json

BASE_DIR = Path(__file__).resolve().parent 

templates = Jinja2Templates(BASE_DIR/"templates")



async def create_profile_service(
        db: AsyncSession , 
        data : CreateProfile , 
        username : str , 
        redis : Redis
        
) -> GetProfile :
    
    cache_key = f"user:profile:{username}"

    cached_profile = await redis.get(cache_key)

    if cached_profile:
        raise HTTPException(
            status_code=409 , 
            detail="user already exists"
        )
    
    existing_user = await db.scalar(
        select(Profile).where(
            Profile.username == username
        )
    )

    if existing_user:
        await redis.set(cache_key , 
                        GetProfile.model_validate(existing_user).model_dump_json() , 
                        ex=30)
        
        raise HTTPException(
            status_code=409 , 
            detail="user already exists"
        )
    
    new_profile = Profile(**data.model_dump())

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    profile_data = GetProfile.model_validate(new_profile)

    await redis.set(
        cache_key, 
        profile_data.model_dump_json() , 
        ex=300
    )

    return profile_data


async def get_profile_service(
        db:AsyncSession , 
        redis: Redis , 
        username : str
) -> GetProfile :
    cached_key = f"user:profile:{username}"

    cached_profile = await redis.get(cached_key)

    if cached_profile:
        return GetProfile.model_validate(json.loads(cached_profile))

    profile = await db.scalar(
        select(Profile).where(Profile.username == username)
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    profile_data = GetProfile.model_validate(profile)

    await redis.set(
        cached_key,
        profile_data.model_dump_json(),
        ex=300,
    )

    return profile_data