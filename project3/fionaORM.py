#NOTE: Drop the address & user_account tables before running this script
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

# DB Connection: create_engine(DBMS_name+driver://fnicdao:Nov05electionDay@fnicdao/UndertheSea)
engine = create_engine("postgresql+psycopg2://postgres:csclass24@localhost/postgres")

#Define Classes/Tables
class Base(DeclarativeBase):
    pass
class Chat(Base):
    __tablename__ = "chat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True) # need to fix UUID
    chtIsActive:Mapped[boolean] = mapped_column(boolean) # fix 
    chtLastMesTimestamp:[date] = mapped_column(date) #fix 

class Message(Base):
    __tablename__ = "message"
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    
