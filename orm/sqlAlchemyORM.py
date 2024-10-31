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

#DB Connection: create_engine(DBMS_name+driver://<username>:<password>@<hostname>/<database_name>)
engine = create_engine("postgresql+psycopg2://postgres:csclass24@localhost/postgres")

#Define Classes/Tables
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str] = mapped_column(String(40))
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str: #represents the object as a string 
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(String(40))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

#Create Tables
Base.metadata.create_all(engine)

#Insert Data
with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")
    session.add_all([spongebob, sandy, patrick])
    session.commit()

# Simple Queries
session = Session(engine)  

print("## User Table Content (1)##")
stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
for user in session.scalars(stmt): #Execute stmt and return the results as scalars
    print(user)

print("\n## User Table Content (2)##")
users = session.query(User)  
for user in users:  
    print("Name: " + user.name, "\nFull Name:" + user.fullname+"\n")

print("## Address Table Content ##")
addresses = session.query(Address)  
for address in addresses:  
    print("Email Address: " + address.email_address)

#Join Query
stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
)
sandy_address = session.scalars(stmt).one()
print("Sandy's Address: " + sandy_address.email_address)

#Updates Sandy's email
sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

#Adds address for Patrick
stmt = select(User).where(User.name == "patrick")
patrick = session.scalars(stmt).one()
patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
session.commit()

#Show updated addresses
print("\n## Address Table Contents - After Update ##")
addresses = session.query(Address)  
for address in addresses:  
    print("Email Address: " + address.email_address)

#Deletes one of Sandy's email addresses (sandy_cheeks@...)
sandy = session.get(User, 2) #2 is the primary key (id)
sandy.addresses.remove(sandy_address)
session.commit()

#Shows updated addresses
print("\n## Address Table Contents - After Delete##")
addresses = session.query(Address)  
for address in addresses:  
    print("Email Address: " + address.email_address)