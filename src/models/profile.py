from src.core.database import Base 
from sqlalchemy import Column , Integer , String 

class Profile(Base):
    __tablename__ = "profile_data"
    id = Column(Integer , primary_key=True , unique=True)
    first_name = Column(String , nullable=False)
    last_name = Column(String , nullable=False)
    username = Column(String , unique=True , nullable=False)
    github  = Column(String , nullable= False)
    email = Column(String , nullable=False)
    linkedin = Column(String , nullable= False )
    portfolio = Column(String )
    x = Column(String , nullable=True)