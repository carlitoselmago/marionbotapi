from db import db

db=db()
con=db.getConnection()

conversations=db.getFlatConversations()

print(conversations)

for msg in conversations:
    print(msg)


with open("chatchat.txt", 'w') as out:
    skip=0
    for texto in conversations:
        if "marion_" in texto:
            skip=2
        if skip>0:
            skip-=1
        else:
            out.write(texto + '\n')
