from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Numeric, DateTime, Enum, Float, func
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
engine = create_engine("postgresql+psycopg2://jhonig:pfLqVAkQEppPWdo7EaGzUvMJNdHPjX2t@localhost:8080/FRIDATING-dev2")
session = Session(engine)  

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
    #actlocgps_x: Mapped[float] = mapped_column(Float, nullable=False)  # Longitude or x-coordinate
    #actlocgps_y: Mapped[float] = mapped_column(Float, nullable=False)  # Latitude or y-coordinate
    userid: Mapped[str] = mapped_column(Integer, ForeignKey("users.usrid"), nullable=False)
    participates_in: Mapped["ParticipatesIn"] = relationship("ParticipatesIn", back_populates="account")
    def __repr__(self) -> str:
        return f"Account(id={self.actID!r}, firstName={self.firstname!r}, lastName={self.lastname!r})"

# Class created by Hannah
class ParticipatesIn(Base):
    __tablename__ = "participatesin"

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
   mesid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   mestext: Mapped[str] = mapped_column(String(200))
   mesdate : Mapped[datetime] = mapped_column(DateTime(timezone=True))
   chatid : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chat.chatid"))
   senderid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("account.actid"))
   chat : Mapped["Chat"] = relationship(back_populates="messages")
  
   def __repr__(self) -> str :
       return f"Message(id={self.id!r}), mesText={self.mestext!r}, mesDate={self.mesdate!r}"

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
       usrid=uuid.UUID("4fc51a78-8d6c-4c64-9c68-a005558a0444"),
       username="TrueB00L",
       email="B00leanFreak45@aol.com",
       passwordhash="kYf8npoLQB@",
       passwordsalt="o@a#&%JE@E1",
       mfatoken="MX%V6-Q3pQg",
       subscription=[Subscription(subtier="Free")]
   )
   user_2 = Users(
       usrid=uuid.UUID("2bca8c6d-a738-4ad6-880d-29cb3af07909"),
       username="JaeMason1234",
       email="masonry7@hotmail.com",
       passwordhash="lQEBgAdu1D5",
       passwordsalt="AJ0%LwrL$z",
       mfatoken="FA!vI_t5mcW",
       subscription=[Subscription(subtier="Premium"), Subscription(subtier='Free')]
   )
   user_3 = Users(
      usrid=uuid.UUID("586c6e9f-2d83-4a09-be8f-03e352eaf0ef"),
      username="mortimersmither",
      email="r&m618@gmail.com",
      passwordhash="B!6H4cBp%9h",
      passwordsalt="ez-F9pk41SP",
      mfatoken="Tm&*2wbt7PY",
      subscription=[Subscription(subtier="Bestie for Life"),
                    Subscription(subtier='Free')]
  )
   user_4 = Users(
      usrid=uuid.UUID("0e607745-f99a-4cbc-aa5c-bc7f2e0c6af3"),
      username="tony_stank88",
      email="male.robo@yahoo.com",
      passwordhash="h!azV^24Y*d",
      passwordsalt="HQipskybvWw",
      mfatoken="8E!A4plaamU",
      subscription=[Subscription(subtier="Bestie for Life"),
                    Subscription(subtier='Free')]
  )
   user_5 = Users(
      usrid=uuid.UUID("f769d227-5e38-4313-80f5-532b81c32185"),
      username="algal",
      email="alex22@gmail.com",
      passwordhash="ddlnv1atwbu2vyfy3g2kf",
      passwordsalt="m4726nasx9gtdqi4mkrj4",
      mfatoken="tddq69utokdat7ydf263h",
      subscription=[Subscription(subtier="Premium"),
                    Subscription(subtier='Free')]
  )
   user_6 = Users(
      usrid=uuid.UUID("ee84defc-0fef-45de-8418-c1cc02a1f90f"),
      username="epic_dude55$",
      email="guy_smith23@aol.com",
      passwordhash="7tfa7ls5upsqwdofntgvs",
      passwordsalt="0xelmdsc413xtk4x0xngz",
      mfatoken="6to1crby5zb7lew5oppge",
      subscription=[Subscription(subtier="Bestie for Life"),
                    Subscription(subtier='Free')]
  )
   user_7 = Users(
      usrid=uuid.UUID("55ff8590-2c7d-4270-8ac6-b8bba37f00a1"),
      username="W0WEnjoyer",
      email="worldofworlds@yahoo.com",
      passwordhash="zk0qv0fmxq6yh85bbw9dg",
      passwordsalt="6g36w54d0m6oklnx19fzv",
      mfatoken="g8b8daj9f9jp967g7wdle",
      subscription=[Subscription(subtier='Free')]
  )
   user_8 = Users(
      usrid=uuid.UUID("40e4de55-3596-4ef7-9ae9-9f763667e531"),
      username="avidTurkey",
      email="turksny2@outlook.com",
      passwordhash="1pl43bwk6e8debo9a2zyj",
      passwordsalt="hufy9borev9lmcfx8lv5j",
      mfatoken="53v1se4qk2obzqobtlo2n",
      subscription=[Subscription(subtier='Free')]
  )
   if actuallyWriteDataToTheDatabase:
       session.add_all([user_1, user_2, user_3, user_4,
                        user_5, user_6, user_7, user_8])
       session.commit()
   # Inserting subs
   subscription1 = Subscription(
       subid = uuid.UUID("05a28cd3-05ab-453e-9ee9-c65d6792ab91"),
       subtier = "Free",
       userid = uuid.UUID("4fc51a78-8d6c-4c64-9c68-a005558a0444")
   )   
   subscription2 = Subscription(
       subid = uuid.UUID("ffd349b2-6c60-4c78-b948-0f5c33ecf3e9"),
       subtier = "Premium",
       subprice = 9.99,
       outstandingbalance = 0.00,
       nextduedate = datetime.datetime.now() + datetime.timedelta(days=45),
       annualbilling = True,
       userid = uuid.UUID("2bca8c6d-a738-4ad6-880d-29cb3af07909")
   )
   subscription3 = Subscription(
       subid = uuid.UUID("cb9aabca-ceb1-40e3-93d7-6b47b27a9b9d"),
       subtier = "Bestie for Life",
       subprice = 49.99,
       outstandingbalance = 0.00,
       nextduedate = datetime.datetime.now() + datetime.timedelta(days=3),
       annualbilling = True,
       userid = uuid.UUID("586c6e9f-2d83-4a09-be8f-03e352eaf0ef")
   )
   subscription4 = Subscription(
       subid = uuid.UUID("3ac10e2e-d2ad-4f3d-90d9-487a1500470a"),
       subtier = "Bestie for Life",
       subprice = 49.99,
       outstandingbalance = 0.00,
       nextduedate = datetime.datetime.now() + datetime.timedelta(days=8),
       annualbilling = True,
       userid = uuid.UUID("0e607745-f99a-4cbc-aa5c-bc7f2e0c6af3")
   )
   subscription5 = Subscription(
       subid = uuid.UUID("886a3851-01e7-4dbf-bcac-c3496f4139d3"),
       subtier = "Premium",
       subprice = 9.99,
       outstandingbalance = 0.00,
       nextduedate = datetime.datetime.now() + datetime.timedelta(days=14),
       annualbilling = True,
       userid = uuid.UUID("f769d227-5e38-4313-80f5-532b81c32185")
   )
   subscription6 = Subscription(
       subid = uuid.UUID("b2442bcd-9bcf-4e21-8ca7-c5bed5fd6854"),
       subtier = "Bestie for Life",
       subprice = 49.99,
       outstandingbalance = 0.00,
       nextduedate = datetime.datetime.now() + datetime.timedelta(days=10),
       annualbilling = True,
       userid = uuid.UUID("ee84defc-0fef-45de-8418-c1cc02a1f90f")
   )
   subscription7 = Subscription(
       subid = uuid.UUID("855ba433-95b4-46d3-b9b5-ba2d46bc4691"),
       subtier = "Free",
       userid = uuid.UUID("55ff8590-2c7d-4270-8ac6-b8bba37f00a1")
   )
   subscription8 = Subscription(
       subid = uuid.UUID("9a8f28cc-001a-4b31-b86a-bf6d96369e57"),
       subtier = "Free",
       userid = uuid.UUID("40e4de55-3596-4ef7-9ae9-9f763667e531")
   )
   if actuallyWriteDataToTheDatabase:
       session.add_all([subscription1, subscription2, subscription3, subscription4, 
                        subscription5,subscription6, subscription7, subscription8])
       session.commit()
 
# Insert data - Fiona 
with Session(engine) as session :  
    chat_1 = Chat(
        chatid = uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
        chtisactive=True,
        chtlastmestimestamp=datetime.datetime.now(),
        messages=[
            Message(mestext="Hi Vision! Do you play Magic the Gathering ?",
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=1),
                    chatid=uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
                    senderid=uuid.UUID("8f11b297-0e06-4d8e-ac29-11b3818c6375")),
            Message(mestext="What is up Wanda! Ya! I just got the new duskmourn deck.",
                    mesdate=datetime.datetime.now(),
                    chatid=uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
                    senderid=uuid.UUID("0090798d-60f8-483c-9516-b4ebe4bd55d3")),
            Message(mestext="Thats awesome! Do you want to get together and play MTG commandard ?",
                    mesdate=datetime.datetime.now(),
                    chatid=uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
                    senderid=uuid.UUID("8f11b297-0e06-4d8e-ac29-11b3818c6375")),
            Message(mestext="Yes! That sounds like fun! ",
                    mesdate=datetime.datetime.now(),
                    chatid=uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
                    senderid=uuid.UUID("0090798d-60f8-483c-9516-b4ebe4bd55d3")),
            Message(mestext="Great! Is it okay for me to invite two of my friends for the game? ",
                    mesdate=datetime.datetime.now(),
                    chatid=uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
                    senderid=uuid.UUID("8f11b297-0e06-4d8e-ac29-11b3818c6375")),
            Message(mestext="Ya! Commander is fun with a group of 4 people  ",
                    mesdate=datetime.datetime.now(),
                    chatid=uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
                    senderid=uuid.UUID("0090798d-60f8-483c-9516-b4ebe4bd55d3"))
        ]
    )
    chat_2 = Chat(
        chatid = uuid.UUID("53e4898d-e1b6-4a38-9721-1982280cdfb6"),
        chtisactive=True,
        chtlastmestimestamp=datetime.datetime.now() - datetime.timedelta(days=4),
        messages=[
            Message(mestext="Hi Emma, what is your favorite music genre ?", 
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=3),
                    chatid=uuid.UUID("53e4898d-e1b6-4a38-9721-1982280cdfb6"),
                    senderid=uuid.UUID("e431e4b0-9a77-4ac6-b4ab-0931fedc8a75")),
            Message(mestext="Hi Erik, I love alternative pop music?", 
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=4),
                    chatid=uuid.UUID("53e4898d-e1b6-4a38-9721-1982280cdfb6"),
                    senderid=uuid.UUID("fe6a275d-03d5-465f-8748-69ad732e3f7b")),
        ]
    )
    chat_3 = Chat(
        chatid = uuid.UUID("cf63c98f-97a6-491c-be7c-1b905dd46c9b"),
        chtisactive=False,
        chtlastmestimestamp=datetime.datetime.now() - datetime.timedelta(days=40),
        messages=[
            Message(mestext="Hi Marisol, do you like running ?",
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=50),
                    chatid=uuid.UUID("cf63c98f-97a6-491c-be7c-1b905dd46c9b"),
                    senderid=uuid.UUID("33d4d3ac-576c-4d11-85b1-bbb9ebaa38e6")),
            Message(mestext="Yes! I just finished the Chicago Marathon" +
                    " and hoping to run in New York next year.", 
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=40),
                    chatid=uuid.UUID("cf63c98f-97a6-491c-be7c-1b905dd46c9b"),
                    senderid=uuid.UUID("65523ca9-4f42-41fc-a8e1-84863ce8fa43")),
        ]
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([chat_1, chat_2, chat_3])
        session.commit()


# Hannah's Insert Data
with Session(engine) as session:
    # Insert account data
    account1 = Account(
        actid = uuid.UUID("6a6a9838-0ead-4988-b9cc-b2cc77cfcd34"),
        bio = "looking for a square dancing partner!",
        firstname = "Stephanie",
        lastname = "Gomez", 
        actstreetaddress = "3670 Charlemaine Dr",
        actcity = "Aurora",
        actstate = "IL",
        #actlocgps_x = 41.73340246308718,
        #actlocgps_y = -88.22654074602464,
        userid = uuid.UUID("3db2bb9a-2418-4258-bbc4-c7ea32b39570") # Need to change depending on drew's info
    )
    account2 = Account(
        actid = uuid.UUID("56d321bd-b33e-4b8a-b8b7-941d3fea8dc7"),
        bio = "Ready to make new friends in Chicago!",
        firstname = "Joseph",
        lastname = "Salvator", 
        actstreetaddress = "403 W 2nd St",
        actcity = "North Platte",
        actstate = "NE",
        #actlocgps_x = 41.13538421572084,
        #actlocgps_y = -100.76768205411464,
        userid = uuid.UUID("3db2bb9a-2418-4258-bbc4-c7ea32b39570") # Need to change depending on drew's info
    )
    account3 = Account(
        actid = uuid.UUID("6ed8a920-0c4c-4ba9-be1d-0fc3fa215338"),
        bio = "Looking for company at sunday night bingo!",
        firstname = "Sammi",
        lastname = "Slante", 
        actstreetaddress = "624 Wyandotte St",
        actcity = "Kansas City",
        actstate = "MO",
        #actlocgps_x = 39.10595603996265,
        #actlocgps_y = -94.58570393663828,
        userid = uuid.UUID("3db2bb9a-2418-4258-bbc4-c7ea32b39570") # Need to change depending on drew's info
    )
    account4 = Account(
        actid = uuid.UUID("16bf9d27-ddcc-4b51-8909-7e381ddb2543"),
        bio = "Love to read, practice yoga, and bike!",
        firstname = "Susan",
        lastname = "Clapper", 
        actstreetaddress = "12980 Silver Fox Dr",
        actcity = "Lemont",
        actstate = "IL",
        #actlocgps_x = 41.653121331513844,
        #actlocgps_y = -87.94838069975592,
        userid = uuid.UUID("3db2bb9a-2418-4258-bbc4-c7ea32b39570") # Need to change depending on drew's info
    )
    account5 = Account(
        actid = uuid.UUID("4842d59b-dfdb-4b71-92b7-3647a1967157"),
        bio = "Ready to meet new friends in Chicago",
        firstname = "Mark",
        lastname = "Sanders", 
        actstreetaddress = "821 N Mohawk St",
        actcity = "Chicago",
        actstate = "IL",
        #actlocgps_x = 41.89728457057297,
        #actlocgps_y = -87.641059003511052,
        userid = uuid.UUID("3db2bb9a-2418-4258-bbc4-c7ea32b39570") # Need to change depending on drew's info
    )
    account6 = Account(
        actid = uuid.UUID("9e0d1b78-1782-4311-b4de-ace18e339ac4"),
        bio = "Football 4 eva ! Bear down.",
        firstname = "Jens",
        lastname = "Peters", 
        actstreetaddress = "821 N Mohawk St",
        actcity = "Chicago",
        actstate = "IL",
        #actlocgps_x = 41.89728457057297,
        #actlocgps_y = -87.641059003511052,
        userid = uuid.UUID("3db2bb9a-2418-4258-bbc4-c7ea32b39570") # Need to change depending on drew's info
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([account1, account2, account3, account4, account5, account6])
        session.commit()

    # Insert participates in
    participatesin1 = ParticipatesIn(
        actid = uuid.UUID("16bf9d27-ddcc-4b51-8909-7e381ddb2543"), # susan & mark
        chatid = uuid.UUID("1f697b04-3fed-47b9-87b6-02f68d04ac21"),
        startdate = datetime.datetime.now() - datetime.timedelta(days=42)
    )
    participatesin2 = ParticipatesIn(
        actid = uuid.UUID("4842d59b-dfdb-4b71-92b7-3647a1967157"), # susan & mark
        chatid = uuid.UUID("1f697b04-3fed-47b9-87b6-02f68d04ac21"),
        startdate = datetime.datetime.now() - datetime.timedelta(days=42)
    )
    participatesin3 = ParticipatesIn(
        actid = uuid.UUID("9e0d1b78-1782-4311-b4de-ace18e339ac4"), # jens & stephanie
        chatid = uuid.UUID("6312dd54-47b0-4d8d-b21c-5cdda64739e6"),
        startdate = datetime.datetime.now() - datetime.timedelta(days=7)
    )
    participatesin4 = ParticipatesIn(
        actid = uuid.UUID("6a6a9838-0ead-4988-b9cc-b2cc77cfcd34"), # jens & stephanie
        chatid = uuid.UUID("6312dd54-47b0-4d8d-b21c-5cdda64739e6"),
        startdate = datetime.datetime.now() - datetime.timedelta(days=7)
    )
    participatesin5 = ParticipatesIn(
        actid = uuid.UUID("9e0d1b78-1782-4311-b4de-ace18e339ac4"), # jens & joseph
        chatid = uuid.UUID("aceec0e9-bf69-4e19-8c4b-5b9a7d3957cd"),
        startdate = datetime.datetime.now() - datetime.timedelta(days=7)
    )
    participatesin6 = ParticipatesIn(
        actid = uuid.UUID("56d321bd-b33e-4b8a-b8b7-941d3fea8dc7"), # jens & joseph
        chatid = uuid.UUID("aceec0e9-bf69-4e19-8c4b-5b9a7d3957cd"),
        startdate = datetime.datetime.now() - datetime.timedelta(days=7)
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([participatesin1, participatesin2, participatesin3, participatesin4, participatesin5, participatesin6])
        session.commit()
    
    # Insert chat data
    chat1 = Chat(
        chatid = uuid.UUID("1f697b04-3fed-47b9-87b6-02f68d04ac21"),
        chtisactive=False,
        chtlastmestimestamp=datetime.datetime.now() - datetime.timedelta(days=40)
    )
    chat2 = Chat(
        chatid = uuid.UUID("6312dd54-47b0-4d8d-b21c-5cdda64739e6"),
        chtisactive=True,
        chtlastmestimestamp=datetime.datetime.now() - datetime.timedelta(hours=2),
        messages=[
            Message(mestext="Hi it's steph! So sorry about that field goal last week.", 
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=3)),
            Message(mestext="Stephanie, lets go to the next game together!!1", 
                    mesdate=datetime.datetime.now()- datetime.timedelta(hours=2)),
        ]
    )
    chat3 = Chat(
        chatid = uuid.UUID("aceec0e9-bf69-4e19-8c4b-5b9a7d3957cd"),
        chtisactive=True,
        chtlastmestimestamp=datetime.datetime.now() - datetime.timedelta(days=2),
        messages=[
            Message(mestext="I'm visiting Chicago next week, lets hang!",
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=3)),
            Message(mestext="sick i'll be your tour guide.", 
                    mesdate=datetime.datetime.now()- datetime.timedelta(days=2)),
        ]
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([chat1, chat2, chat3])
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
    print(f"""[Josh] Card {record.num} is being used to cover subscription for tier {record.subscription.subtier} (id={record.subid}), next due {record.subscription.nextduedate.strftime("%B %d, %Y")}""")


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


# Join Query  by Fiona 
# This join query looks at a specific chat that IS active and 
# is using the chat id for a specific chat.  It will print out 
# the conversation (messages) are between the user_accounts.

print("\n## Join Query -  Fiona  ##")
stmt = (
    select(Message)
    .join(Message.chat)
    .where(Chat.chtisactive == True)
    .where(Chat.chatid == uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"))
    .order_by(Message.chatid)
    .order_by(Message.mesid)
)

for record in session.scalars(stmt) :
    print(f"""[Fiona] message id={record.mesid} chat_id={record.chatid} 
            message date={record.mesdate} 
            message Text={record.mestext} """)
    
# Join Query by Hannah 
# This join query displays the account information for all accounts who have participated in more than 1 chat.

print("\n## Join Query - Hannah ##")
stmt = (
    select(Account)
    .join(ParticipatesIn, Account.actid == ParticipatesIn.actid)
    .group_by(Account.actid)
    .having(func.count(ParticipatesIn.chatid) > 1)
    .order_by(Account.actid)
)

for record in session.scalars(stmt):
    print(f"""[Hannah] Account ID={record.actid} 
            First Name={record.firstname} 
            Last Name={record.lastname}""")