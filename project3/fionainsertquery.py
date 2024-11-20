
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
    if actuallyWriteDataToTheDatabase:
        session.add_all([chat_1, chat_2, chat_3])
        session.commit()

# Join Query -Fiona 
# This join query looks at the chats that ARE active and see what their 
# conversation (messages) are between the user_accounts.

print("\n## Join Query -  Fiona  ##")
stmt = (
    select(Message)
    .join(Message.chat)
    .where(Chat.chtisactive == True)
    .order_by(Message.chatid)
    .order_by(Message.mesid)
)

for record in session.scalars(stmt) :
    # print(f"message id={record.id}")
    print(f"""[Fiona] message id={record.mesid} chatid={record.chatid} 
            message date={record.mesdate} 
            message Text={record.mestext}""")    
