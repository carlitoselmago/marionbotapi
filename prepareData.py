from db import db

db=db()
con=db.getConnection()

conversations=db.getAllConversations()[0]

with open('data/marion/chatDB.txt', 'w') as f:
    for item in conversations:
        #print (item)

        f.write("%s\n" % item.strip())
