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

# Classes created by Fiona & Hannah
class Chat(Base):
   __tablename__ = "chat"
  
   chatid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
   chtisactive: Mapped[bool]
   chtlastmestimestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False))
   # Relationships
#    participants: Mapped["ParticipatesIn"] = relationship("ParticipatesIn", back_populates="chat")
   # referernce to messages
   messages : Mapped[List["Message"]] = relationship(
       back_populates="chat", cascade="all, delete-orphan"
   )
   def __repr__(self) -> str: #represent the object as a string
       return f"Chat (id = {self.id!r}, chatIsActive{self.chtisactive!r}, chtLastMesTimestamp{self.chtlastmestimestamp!r})"


# Class created by Fiona
class Message(Base):
   __tablename__ = "message"
   mesid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
   mestext: Mapped[str] = mapped_column(String(200))
   mesdate : Mapped[datetime] = mapped_column(DateTime(timezone=True))
   chatid : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat.chatid"))
   chat : Mapped["Chat"] = relationship(back_populates="messages")
  
   def __repr__(self) -> str :
       return f"Message(id={self.id!r}), mesText={self.mestext!r}, mesDate={self.mesdate!r}"

    
#Create Tables
Base.metadata.create_all(engine)

# Insert data - Fiona 
with Session(engine) as session :  
    chat_1 = Chat(
        chatid = uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
        chtisactive=True,
        chtlastmestimestamp=datetime.datetime.now(),
        messages=[
            Message(mesid=uuid.UUID("03a9c586-a4d5-4089-aa34-1198ea8fa3bc"), mestext="Hi Vision! Do you play Magic the Gathering ?",
                    mesdate=datetime.datetime.now()- timedelta(days=1)),
            Message(mesid=uuid.UUID("0c6a58a0-5fc0-44a6-8c39-54c14a8d553f"), mestext="What is up Wanda! Ya! I just got the new duskmourn deck.",
                    mesdate=datetime.datetime.now()),
            Message(mesid=uuid.UUID("081195c2-9058-4e10-8316-ed2a5cd69856"), mestext="Thats awesome! Do you want to get together and play MTG commandard ?",
                    mesdate=datetime.datetime.now()),
            Message(mesid=uuid.UUID("8fdcd137-5917-4507-9c46-d139503e76ea"), mestext="Yes! That sounds like fun! ",
                    mesdate=datetime.datetime.now()),
            Message(mesid=uuid.UUID("549e76df-c525-4153-a450-51d81142bb5d"), mestext="Great! Is it okay for me to invite two of my friends for the game? ",
                    mesdate=datetime.datetime.now()),
            Message(mesid=uuid.UUID("f4bde6c9-4999-45b7-b9b2-577574421334"), mestext="Ya! Commander is fun with a group of 4 people  ",
                    mesdate=datetime.datetime.now())
            
        ]
    )
    chat_2 = Chat(
        chatid = uuid.UUID("53e4898d-e1b6-4a38-9721-1982280cdfb6"),
        chtisactive=False,
        chtlastmestimestamp=datetime.datetime.now() - timedelta(days=4),
        messages=[
            Message(mesid=uuid.UUID("065b95e9-63de-42bf-bf8c-6aec3f810485"), mestext="Hi Emma, what is your favorite music genre ?", 
                    mesdate=datetime.datetime.now()- timedelta(days=3)),
            Message(mesid=uuid.UUID("939f7ec2-0eca-4e51-a5a7-a919fef14e7f"), mestext="Hi Erik, I love alternative pop music?", 
                    mesdate=datetime.datetime.now()- timedelta(days=4)),
        ]
    )
    chat_3 = Chat(
        chatid = uuid.UUID("cf63c98f-97a6-491c-be7c-1b905dd46c9b"),
        chtisactive=False,
        chtlastmestimestamp=datetime.datetime.now() - timedelta(days=40),
        messages=[
            Message(mesid=uuid.UUID("6199e51a-0add-484c-96e8-25aa16a9b9a1"), mestext="Hi Marisol, do you like running ?",
                    mesdate=datetime.datetime.now()- timedelta(days=50)),
            Message(mesid=uuid.UUID("1cb5c60b-50cc-45d8-ab36-8da48e98f3f5"), mestext="Yes! I just finished the Chicago Marathon" +
                    " and hoping to run in New York next year.", 
                    mesdate=datetime.datetime.now()- timedelta(days=40)),
        ]
    )
    session.add_all([chat_1, chat_2, chat_3])
    session.commit()


# # # Simple Queries
session = Session(engine)

# print("\n## Chat Table Content ##")
# chats = session.query(Chat)  
# for chat in chats:  
#     print("id: " + str(chat.id),"date: " + str(chat.chtLastMesTimestamp),
#           "\nIs the chat active?:" + str(chat.chtIsActive)+"\n")

# print("\n ## Message Table Content ##")
# messages = session.query(Message)
# for message in messages:
#     print("id=" +str(message.id) + " chat_id =" +str(message.chat_id),  
#           "\n message text = " + message.mesText + "\n")

# # Join Query -Fiona 
# # This join query looks at the chats that ARE active and see what their 
# # conversation (messages) are between the user_accounts.

# print("\n## Join Query -  Fiona  ##")
# stmt = (
#     select(Message)
#     .join(Message.chat)
#     .where(Chat.chtIsActive == True)
#     .order_by(Message.id)
# )


# for record in session.scalars(stmt) :
#     # print(f"message id={record.id}")
#     print(f"message id={record.id} chat_id={record.chat_id} 
#           \n  message date={record.mesDate} 
#           \n  message Text={record.mesText} \n\n")
    
# join Query 
print("\n## Join Query -  Fiona  ##")
stmt = (
    select(Message)
    .join(Message.chat)
    .where(Chat.chtisactive == True)
    .order_by(Message.chatid)
    .order_by(Message.mesid)
)
# vision_message = session.scalars(stmt).one()
# print("Vision's Message " + vision_message.mesText)

for record in session.scalars(stmt) :
    # print(f"message id={record.id}")
    print(f"message id={record.mesid} chat_id={record.chatid} \n  message date={record.mesdate} \n  message Text={record.mestext} \n\n")