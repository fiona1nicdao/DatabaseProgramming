
# Insert data - Fiona 
with Session(engine) as session :  
    chat_1 = Chat(
        chatid = uuid.UUID("294441f3-87d3-4989-96bd-9dfb7c9d5325"),
        chtisactive=True,
        chtlastmestimestamp=datetime.datetime.now(),
        messages=[
            Message(mestext="Hi Vision! Do you play Magic the Gathering ?",
                    mesdate=datetime.datetime.now()- timedelta(days=1)),
            Message(mestext="What is up Wanda! Ya! I just got the new duskmourn deck.",
                    mesdate=datetime.datetime.now()),
            Message(mestext="Thats awesome! Do you want to get together and play MTG commandard ?",
                    mesdate=datetime.datetime.now()),
            Message(mestext="Yes! That sounds like fun! ",
                    mesdate=datetime.datetime.now()),
            Message(mestext="Great! Is it okay for me to invite two of my friends for the game? ",
                    mesdate=datetime.datetime.now()),
            Message(mestext="Ya! Commander is fun with a group of 4 people  ",
                    mesdate=datetime.datetime.now())
        ]
    )
    chat_2 = Chat(
        chatid = uuid.UUID("53e4898d-e1b6-4a38-9721-1982280cdfb6"),
        chtisactive=False,
        chtlastmestimestamp=datetime.datetime.now() - timedelta(days=4),
        messages=[
            Message(mestext="Hi Emma, what is your favorite music genre ?", 
                    mesdate=datetime.datetime.now()- timedelta(days=3)),
            Message(mestext="Hi Erik, I love alternative pop music?", 
                    mesdate=datetime.datetime.now()- timedelta(days=4)),
        ]
    )
    chat_3 = Chat(
        chatid = uuid.UUID("cf63c98f-97a6-491c-be7c-1b905dd46c9b"),
        chtisactive=False,
        chtlastmestimestamp=datetime.datetime.now() - timedelta(days=40),
        messages=[
            Message(mestext="Hi Marisol, do you like running ?",
                    mesdate=datetime.datetime.now()- timedelta(days=50)),
            Message(mestext="Yes! I just finished the Chicago Marathon" +
                    " and hoping to run in New York next year.", 
                    mesdate=datetime.datetime.now()- timedelta(days=40)),
        ]
    )
    if actuallyWriteDataToTheDatabase:
        session.add_all([chat_1, chat_2, chat_3])
        session.commit()