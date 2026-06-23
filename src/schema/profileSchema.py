from pydantic import BaseModel, ConfigDict , Field , EmailStr

class CreateProfile(BaseModel):
    first_name : str = Field(max_length=20 , min_length=3)
    last_name : str = Field(max_length=20 , min_length=3)
    username : str 
    github : str 
    email : EmailStr
    linkedin : str 
    portfolio : str | None = None 
    x : str | None = None


class GetProfile(BaseModel):
    id : int 
    first_name : str = Field(max_length=20 , min_length=3)
    last_name : str = Field(max_length=20 , min_length=3)
    username : str 
    github : str 
    email : EmailStr
    linkedin : str 
    portfolio : str | None = None 
    x : str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateProfile(BaseModel):
    first_name : str = Field(max_length=20 , min_length=3)
    last_name : str = Field(max_length=20 , min_length=3)
    username : str 
    github : str 
    email : EmailStr
    linkedin : str 
    portfolio : str | None = None 
    x : str | None = None


