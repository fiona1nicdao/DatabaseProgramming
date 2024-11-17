#NOTE: Drop the address & user_account tables before running this script
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
# from sqlalchemy import TypeEngine
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Any
from typing import Dict
from typing import Type

import datetime
from datetime import timedelta
import uuid



# DB Connection: create_engine(DBMS_name+driver://fnicdao:Nov05electionDay@fnicdao/UndertheSea)
engine = create_engine("postgresql+psycopg2://postgres:csclass24@localhost/postgres")

# Define Classes/Tables
class Base(DeclarativeBase):
    pass
class Chat(Base):
    __tablename__ = "chat"
    
    # chatID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    chtIsActive : Mapped[bool] = mapped_column(Boolean) # fix 
    chtLastMesTimestamp : Mapped[datetime] = mapped_column(DateTime(timezone=True)) #fix 
    # referernce to messages 
    messages : Mapped[List["Message"]] = relationship(
        back_populates="chat", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str: #represent the object as a string
        return f"Chat (id = {self.id!r}, chatIsActive{self.chtIsActive!r},
            chtLastMesTimestamp{self.chtLastMesTimestamp!r})"

class Message(Base):
    __tablename__ = "message"
    # chatID: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    mesText: Mapped[str] = mapped_column(String(200))
    mesDate : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    chat_id : Mapped[int] = mapped_column(Integer, ForeignKey("chat.id"))
    chat : Mapped["Chat"] = relationship(back_populates="messages")
    
    def __repr__(self) -> str : 
        return f"Message(id={self.id!r}), mesText={self.mesText!r}, 
            mesDate={self.mesDate!r}"
    
#Create Tables
Base.metadata.create_all(engine)

#Insert Data -  Fiona 
with Session(engine) as session :  
    chat_1 = Chat(
        chtIsActive=True,
        chtLastMesTimestamp=datetime.datetime.now(),
        messages=[
            Message(mesText="Hi Vision! Do you play Magic the Gathering ?",
                    mesDate=datetime.datetime.now()- timedelta(days=1)),
            Message(mesText="What is up Wanda! Ya! I just got the new duskmourn deck.",
                    mesDate=datetime.datetime.now())
        ]
    )
    chat_2 = Chat(
        chtIsActive=True,
        chtLastMesTimestamp=datetime.datetime.now() - timedelta(days=4),
        messages=[
            Message(mesText="Hi Emma, what is your favorite music genre ?", 
                    mesDate=datetime.datetime.now()- timedelta(days=3)),
            Message(mesText="Hi Erik, I love alternative pop music?", 
                    mesDate=datetime.datetime.now()- timedelta(days=4)),
        ]
    )
    chat_3 = Chat(
        chtIsActive=False,
        chtLastMesTimestamp=datetime.datetime.now() - timedelta(days=40),
        messages=[
            Message(mesText="Hi Marisol, do you like running ?",
                    mesDate=datetime.datetime.now()- timedelta(days=50)),
            Message(mesText="Yes! I just finished the Chicago Marathon" +
                    " and hoping to run in New York next year.", 
                    mesDate=datetime.datetime.now()- timedelta(days=40)),
        ]
    )
    session.add_all([chat_1, chat_2, chat_3])
    session.commit()

# # Simple Queries
session = Session(engine)

print("\n## Chat Table Content ##")
chats = session.query(Chat)  
for chat in chats:  
    print("id: " + str(chat.id),"date: " + str(chat.chtLastMesTimestamp),
          "\nIs the chat active?:" + str(chat.chtIsActive)+"\n")

print("\n ## Message Table Content ##")
messages = session.query(Message)
for message in messages:
    print("id=" +str(message.id) + " chat_id =" +str(message.chat_id),  
          "\n message text = " + message.mesText + "\n")
    
# join Query 
print("\n## Join Query -  Fiona  ##")
stmt = (
    select(Message)
    .join(Message.chat)
    .where(Chat.chtIsActive == False)
    .order_by(Message.id)
)
# vision_message = session.scalars(stmt).one()
# print("Vision's Message " + vision_message.mesText)

for record in session.scalars(stmt) :
    # print(f"message id={record.id}")
    print(f"message id={record.id} chat_id={record.chat_id} 
          \n  message date={record.mesDate} 
          \n  message Text={record.mesText} \n\n")