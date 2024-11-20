# Join Query 
# This join query looks at a specific chat that IS active and 
# is using the chat id for a specific chat.  It will print out 
# the conversation (messages) are between the user_accounts.

print("\n## Join Query -  Fiona  ##")
stmt = (
    select(Message)
    .join(Message.chat)
    .where(Chat.chtisactive == True)
    .where(Chat.chatid == "294441f3-87d3-4989-96bd-9dfb7c9d5325")
    .order_by(Message.chatid)
    .order_by(Message.mesid)
)

for record in session.scalars(stmt) :
    print(f"""message id={record.mesid} chat_id={record.chatid} 
          \n  message date={record.mesdate} 
          \n  message Text={record.mestext} \n\n""")