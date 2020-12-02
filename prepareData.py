from db import db

db=db()
con=db.getConnection()

conversations=db.getAllConversations()

with open('data/marion/chatDB.txt', 'w') as f:
    for conv in conversations:
        print (len(conv))
        for item in conv:


            f.write("%s\n" % item.strip())
