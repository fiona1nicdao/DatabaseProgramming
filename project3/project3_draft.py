from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Numeric, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime 
import enum
import pdb

# IMPORTANT! IMPORTANT! IMPORTANT! 
# Change this to TRUE if you want to attempt to write data to the db!
actuallyWriteDataToTheDatabase = False
# IMPORTANT! IMPORTANT! IMPORTANT! 
# IMPORTANT! IMPORTANT! IMPORTANT! 

# Database connection
engine = create_engine("postgresql+psycopg2://jhonig:PASSWORD@localhost:8080/FRIDATING-dev")

class Base(DeclarativeBase):
    pass

# Class created by Drew; Defining User class/table
class Users(Base):
    __tablename__ = "users"

    usrid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(96))
    passwordhash: Mapped[str] = mapped_column(String(256))
    passwordsalt: Mapped[str] = mapped_column(String(256))
    mfatoken: Mapped[str] = mapped_column(String(64))
    subscription: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.userID!r}, username={self.username!r}, email={self.email!r})"

# Class created by Josh; define Subscription table
class Subscription(Base):
    __tablename__ = "subscription"

    subid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    subtier: Mapped[str] = mapped_column(String(64))
    subprice: Mapped[Numeric] = mapped_column(Numeric, nullable=True)
    outstandingbalance: Mapped[Numeric] = mapped_column(Numeric, nullable=True)
    nextduedate: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=True) # https://stackoverflow.com/a/75364468/11467212
    annualbilling: Mapped[Optional[bool]] # Since bool is a native python type, sqlalchemy will figure this out # https://stackoverflow.com/a/76499049/11467212
    userid: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.usrid"))

    paymentmethods: Mapped[List["paymentmethod"]] = relationship(
        back_populates="subscription", cascade="all, delete-orphan"
    )

    user: Mapped["Users"] = relationship(back_populates="subscription")

    def __repr__(self) -> str:
        return f"""Subscription(
            id={self.subid!r}, subtier={self.subtier!r}, subprice={self.subprice!r}, 
            nextduedate={self.nextduedate!r}, annualbilling={self.annualbilling!r}, 
            userid={self.userid!r})"""

# Class created by Josh; defines enum for use in paymnetmethod
class payment_type(enum.Enum):
    credit = 'credit'
    debit = 'debit'
    thirdParty = 'thirdParty'

# Class created by Josh; define paymentmethod table
class paymentmethod(Base):
    __tablename__ = "paymentmethod"
    
    pmtid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    subid: Mapped[uuid.UUID] = mapped_column(ForeignKey("subscription.subid"))
    pmttype = mapped_column(Enum(payment_type))
    num: Mapped[Numeric] = mapped_column(Numeric, nullable=True)
    cvv: Mapped[Numeric] = mapped_column(Numeric, nullable=True)
    expiration: Mapped[str] = mapped_column(String(16), nullable=True)
    pmtstreetaddr: Mapped[str] = mapped_column(String(128), nullable=True)
    pmtcity: Mapped[str] = mapped_column(String(64), nullable=True)
    pmtstate: Mapped[str] = mapped_column(String(64), nullable=True)
    pmtzipcode: Mapped[str] = mapped_column(String(64), nullable=True)
    androidpay: Mapped[str] = mapped_column(String(128), nullable=True)
    applepay: Mapped[str] = mapped_column(String(128), nullable=True)
    paypal: Mapped[str] = mapped_column(String(128), nullable=True)

    subscription: Mapped["Subscription"] = relationship(back_populates="paymentmethods")

    def __repr__(self) -> str:
        return f"""paymentMethod(
            pmtid={self.pmtid!r}, subid={self.subid!r}, pmtType={self.pmttype!r},
            num={self.num!r}, cvv={self.cvv!r}, expiration={self.expiration!r}, 
            pmtstreetaddr={self.pmtstreetaddr!r}, pmtcity={self.pmtcity!r}, 
            pmtstate={self.pmtstate!r}, pmtzipcode={self.pmtzipcode!r}, 
            androidpay={self.androidpay!r}, applepay={self.applepay!r}, paypal={self.paypal!r})"""
    

# Classes created by Hannah
class Account(Base):
    __tablename__ = "account"

    actid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    bio: Mapped[str] = mapped_column(String(300))
    firstname: Mapped[str] = mapped_column(String(32), nullable=False)
    lastname: Mapped[str] = mapped_column(String(32))
    actstreetaddress: Mapped[str] = mapped_column(String(128), nullable=False)
    actcity: Mapped[str] = mapped_column(String(64), nullable=False)
    actstate: Mapped[str] = mapped_column(String(64), nullable=False)
    #actLocGPS: Mapped["Geometry"] = mapped_column(Geometry("POINT"), nullable=False)
    userid: Mapped[str] = mapped_column(Integer, ForeignKey("users.usrid"), nullable=False)
    participates_in: Mapped["ParticipatesIn"] = relationship("ParticipatesIn", back_populates="account")
    def __repr__(self) -> str:
        return f"Account(id={self.actID!r}, firstName={self.firstname!r}, lastName={self.lastname!r})"

# Class created by Hannah
class ParticipatesIn(Base):
    __tablename__ = "participatesIn"


    actid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("account.actid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    chatid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat.chatid", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    startdate: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=True)


    # Relationships
    account: Mapped["Account"] = relationship("Account", back_populates="participates_in")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="participants")

    def __repr__(self) -> str: return f"ParticipatesIn(actID={self.actid!r}, chatID={self.chatid!r})"

# Classes created by Fiona & Hannah
class Chat(Base):
   __tablename__ = "chat"
  
   chatid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
   chtisactive: Mapped[bool]
   chtlastmestimestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False))
   # Relationships
   participants: Mapped["ParticipatesIn"] = relationship("ParticipatesIn", back_populates="chat")
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
   chat_id : Mapped[uuid.UUID] = mapped_column(Integer, ForeignKey("chat.chatid"))
   chat : Mapped["Chat"] = relationship(back_populates="messages")
  
   def __repr__(self) -> str :
       return f"Message(id={self.id!r}), mesText={self.mestext!r}, mesDate={self.mesdate!r}"





session = Session(engine)  

# Insert data - Josh
with Session(engine) as session:
    # Insert subscriptions
    subscription1 = Subscription(
        subid = uuid.UUID("ba2a5760-0ead-4988-b9cc-b2cc77cfcd34"),
        subtier = "Premium",
        subprice = 9.99,
        outstandingbalance = 0.00, 
        nextduedate = datetime.datetime.now() + datetime.timedelta(days=6),
        annualbilling = False,
        userid = uuid.UUID("3db2bb9a-2418-4258-bbc4-c7ea32b39570")
    )
    subscription2 = Subscription(
        subid = uuid.UUID("ef7b5717-96f2-42b4-8bb2-23ae9172ff65"),
        subtier = "Bestie for Life",
        subprice = 49.99,
        outstandingbalance = 0.00, 
        nextduedate = datetime.datetime.now() + datetime.timedelta(days=3) + datetime.timedelta(hours=5),
        annualbilling = False,
        userid = uuid.UUID("a87b4c9b-f164-4e4b-99a4-2d64f2212ca7")
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([subscription1, subscription2])
        session.commit()

    # Insert payment methods
    pmtmethod1 = paymentmethod(
        subid = uuid.UUID("ba2a5760-0ead-4988-b9cc-b2cc77cfcd34"),
        pmttype = payment_type.thirdParty,
        paypal = "somePaypalPaymentAPIKeyGoesHere"
    )
    pmtmethod2 = paymentmethod(
        subid = uuid.UUID("ef7b5717-96f2-42b4-8bb2-23ae9172ff65"),
        pmttype = payment_type.credit,
        num = 4381946282957154,
        cvv = 123, 
        expiration = "05/25",
        pmtstreetaddr = "1 N Oak St",
        pmtcity = "Anytown",
        pmtstate = "IL",
        pmtzipcode = "60601"
    )
    pmtmethod3 = paymentmethod(
        subid = uuid.UUID("ef7b5717-96f2-42b4-8bb2-23ae9172ff65"),
        pmttype = payment_type.credit,
        num = 6195016491745164,
        cvv = 321, 
        expiration = "01/26",
        pmtstreetaddr = "405 S Railroad Ave",
        pmtcity = "Cornfieldia",
        pmtstate = "IN",
        pmtzipcode = "43052"
    )
    pmtmethod4 = paymentmethod(
        subid = uuid.UUID("ef7b5717-96f2-42b4-8bb2-23ae9172ff65"),
        pmttype = payment_type.credit,
        num = 1750161067181961,
        cvv = 159, 
        expiration = "12/24",
        pmtstreetaddr = "8000 University Rd",
        pmtcity = "Lafayette",
        pmtstate = "IN",
        pmtzipcode = "47904"
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([pmtmethod1, pmtmethod2, pmtmethod3, pmtmethod4])
        session.commit()

# Insert data - Drew
with Session(engine) as session:
    user_1 = Users(
        usrid=uuid.UUID("21bb1aa8-6dbf-4e14-ace7-01c4e8df2296"),
        username="True",
        email="tyler.caldwell45@aol.com",
        passwordhash="50d9bff2316afe080b1b687f1adf82b5",
        passwordsalt="0e36f46fd7312733c821b916fb76a5cd",
        mfatoken="d537d90960f22c441bd0bd2ce9ccf3af",
        subscription=[Subscription(subtier="Free")]
    )
    user_2 = Users(
        usrid=uuid.UUID("829ebcd5-d57f-434d-931b-aec167cf5c03"),
        username="JayMorrow87",
        email="jason.morrow87@hotmail.com",
        passwordhash="fc5e038d38a57032085441e7fe7010b0",
        passwordsalt="8a68587ce598d58bc09b6d07c5d298b8",
        mfatoken="11d9156385fce85c1a66956536187d50",
        subscription=[Subscription(subtier="Premium"), Subscription(subtier='Free')]
    )
    user_3 = Users(
       usrid=uuid.UUID("94ab690c-3864-407b-8354-4e606ee0cc70"),
       username="jsmith",
       email="jsmith2618@gmail.com",
       passwordhash="7c6a180b36896a0a8c02787eeafb0e4c",
       passwordsalt="f319ba7e7e4d56601091ce3789480f44",
       mfatoken="5cdc5c9973e3527741f698d5588eca72",
       subscription=[Subscription(subtier="Bestie for Life"),
                     Subscription(subtier='Free')]
   )
    user_4 = Users(
       usrid=uuid.UUID("90d7a0ae-b451-400f-bc12-784817309921"),
       username="tony1",
       email="tony2@yahoo.com",
       passwordhash="2304d4770a72d09106045fea654c4188",
       passwordsalt="bbf97fe32f28639002ce2d24d1c75d0b",
       mfatoken="289409826efa4486adb71cc715cc3ffa",
       subscription=[Subscription(subtier="Bestie for Life"),
                     Subscription(subtier='Free')]
   )
    if actuallyWriteDataToTheDatabase:
        session.add_all([user_1, user_2, user_3, user_4])
        session.commit()
    # Inserting subs
    subscription2 = Subscription(
        subid = uuid.UUID("b307e71b-bbe4-4055-b488-d01ab711a5bd"),
        subtier = "Premium",
        subprice = 9.99,
        outstandingbalance = 0.00, 
        nextduedate = datetime.datetime.now() + datetime.timedelta(days=6),
        annualbilling = True,
        userid = uuid.UUID("829ebcd5-d57f-434d-931b-aec167cf5c03")
    )
    subscription3 = Subscription(
        subid = uuid.UUID("4f36fd46-c84c-4d7c-868b-85532e580dab"),
        subtier = "Bestie for Life",
        subprice = 49.99,
        outstandingbalance = 0.00, 
        nextduedate = datetime.datetime.now() + datetime.timedelta(days=8),
        annualbilling = True,
        userid = uuid.UUID("94ab690c-3864-407b-8354-4e606ee0cc70")
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([subscription2, subscription3])
        session.commit()
    

# Query and output by Josh
# This query shows which credit cards are being used to cover which non-free-tier subscriptions. 
statement = (
    select(paymentmethod)
    .join(paymentmethod.subscription)
    .where(
        Subscription.subtier != "Free" and
        paymentmethod.pmttype != payment_type.thirdParty
    )
    .order_by(Subscription.nextduedate)
)
for record in session.scalars(statement):
    print(f"""[Josh] Card {record.num} is being used to cover subscription with id={record.subid}""")
    #pdb.set_trace()

# Insert data - Fiona 
with Session(engine) as session :  
    chat_1 = Chat(
        chatid = uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
        chtisactive=True,
        chtLastMesTimestamp=datetime.datetime.now(),
        messages=[
            Message(mesid=uuid.UUID("03a9c586-a4d5-4089-aa34-1198ea8fa3bc"), mesText="Hi Vision! Do you play Magic the Gathering ?",
                    mesDate=datetime.datetime.now()- timedelta(days=1)),
            Message(mesid=uuid.UUID("892679d7-2aac-4dac-940f-1db131c91535"), mesText="What is up Wanda! Ya! I just got the new duskmourn deck.",
                    mesDate=datetime.datetime.now())
        ]
    )
    chat_2 = Chat(
        chatid = uuid.UUID("53e4898d-e1b6-4a38-9721-1982280cdfb6"),
        chtisactive=True,
        chtLastMesTimestamp=datetime.datetime.now() - timedelta(days=4),
        messages=[
            Message(mesid=uuid.UUID("065b95e9-63de-42bf-bf8c-6aec3f810485"), mesText="Hi Emma, what is your favorite music genre ?", 
                    mesDate=datetime.datetime.now()- timedelta(days=3)),
            Message(mesid=uuid.UUID("939f7ec2-0eca-4e51-a5a7-a919fef14e7f"), mesText="Hi Erik, I love alternative pop music?", 
                    mesDate=datetime.datetime.now()- timedelta(days=4)),
        ]
    )
    chat_3 = Chat(
        chatid = uuid.UUID("cf63c98f-97a6-491c-be7c-1b905dd46c9b"),
        chtisactive=False,
        chtLastMesTimestamp=datetime.datetime.now() - timedelta(days=40),
        messages=[
            Message(mesid=uuid.UUID("6199e51a-0add-484c-96e8-25aa16a9b9a1"), mesText="Hi Marisol, do you like running ?",
                    mesDate=datetime.datetime.now()- timedelta(days=50)),
            Message(mesid=uuid.UUID("1cb5c60b-50cc-45d8-ab36-8da48e98f3f5"), mesText="Yes! I just finished the Chicago Marathon" +
                    " and hoping to run in New York next year.", 
                    mesDate=datetime.datetime.now()- timedelta(days=40)),
        ]
    )
    session.add_all([chat_1, chat_2, chat_3])
    session.commit()

# Query and output by Drew
# This query shows which username has a paid subscription, and what type.
statement = (
    select(Users)
    .join(Users.subscription)
    .where(
        Subscription.subtier != "Free"
    )
    .order_by(Subscription.subprice)
)

for record in session.scalars(statement):
    print(f"[Drew] User {record.username} currently has {record.subscription}")

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
    .where(Chat.chtisactive == True)
    .order_by(Message.id)
)
# vision_message = session.scalars(stmt).one()
# print("Vision's Message " + vision_message.mesText)

for record in session.scalars(stmt) :
    # print(f"message id={record.id}")
    print(f"message id={record.id} chat_id={record.chat_id} 
          \n  message date={record.mesdate} 
          \n  message Text={record.mestext} \n\n")