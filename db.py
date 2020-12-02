import pymysql
import pymysql.cursors
from sqlalchemy.sql import func
import time

class db():

    db=False

    def __init__(self):
        print("DB STARTED")
        # Open database connection

    def getConnection(self):
        return pymysql.connect("localhost","admin","kdjkdk23k3dk-ddd2","marionbot",cursorclass=pymysql.cursors.DictCursor,charset="utf8mb4")

    def getUsers(self):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT * FROM  people"
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return results

    def getChats(self):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT c.id, c.userid , p.name, c.notseen FROM chats c LEFT JOIN `people` p ON c.userid = p.id WHERE `archived`=0 ORDER BY c.lastupdated DESC"
        #sql = "SELECT * FROM chats"
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return results

    def userExists(self,username):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT * FROM  people WHERE name='%s'" % \
        (username)

        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        print("len(results)",len(results))
        if len(results)>0:
            return results
        else:
            return False

    def getUserName(self,userid):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT name FROM  people WHERE id='%d'" % \
        (userid)
        cursor.execute(sql)
        results = cursor.fetchone()
        db.close()
        return results["name"]

    def getUserChatId(self,userid):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT id FROM chats WHERE userid=%d" % \
        (userid)
        cursor.execute(sql)
        results = cursor.fetchone()
        db.close()
        return results["id"]

    def checkUserPassword(self,user,password):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT * FROM  people WHERE name='%s' AND password='%s'" % \
        (user,password)

        cursor.execute(sql)

        results = cursor.fetchall()
        db.close()
        if len(results)>0:
            if results[0]["name"]==user:
                if results[0]["password"]==password:
                    return results[0]
        return False


    def getMessages(self,chatid,lastMsgDate):

        db=self.getConnection()
        cursor = db.cursor()
        #sql = "SELECT * FROM  messages WHERE `from` = "+str(chatid)
        if lastMsgDate:
            sql = "SELECT m.id, m.date, m.from, m.chat, m.text, m.tipo, p.name FROM messages m LEFT JOIN `people` p ON m.from = p.id WHERE `chat` = "+str(chatid)+" AND date>"+str(lastMsgDate)+" ORDER BY m.date"
        else:
            sql = "SELECT m.id, m.date, m.from, m.chat, m.text, m.tipo, p.name FROM messages m LEFT JOIN `people` p ON m.from = p.id WHERE `chat` = "+str(chatid)+" ORDER BY m.date"

        cursor.execute(sql)
        results = cursor.fetchall()
        # Commit your changes in the database
        db.close()
        return results

    def addunseen(self,chatid):
        db=self.getConnection()

        cursor = db.cursor()
        sql = "UPDATE chats SET `notseen` = `notseen` + 1 WHERE id="+str(chatid)
        cursor.execute(sql)
        db.commit()
        # disconnect from server
        db.close()

    def removeNotSeen(self,chatid):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "UPDATE chats SET `notseen` = 0 WHERE id="+str(chatid)
        cursor.execute(sql)
        db.commit()
        # disconnect from server
        db.close()

    def archiveChat(self,chatid):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "UPDATE chats SET `archived` = 1 WHERE id="+str(chatid)
        cursor.execute(sql)
        db.commit()
        # disconnect from server
        db.close()

    def saveMessage(self,user,chat,msg,tipo=0):
        db=self.getConnection()
        cursor = db.cursor()
        #text=db.escape(msg)
        text=msg
        sql = "INSERT INTO messages( \
           `date`,`text` ,`from`,`chat`,`tipo`) \
           VALUES (%s, %s, %s,%s,%s)"

        cursor.execute(sql,(int(time.time()), text, int(user),int(chat),int(tipo)))
        db.commit()
        if user>1:
            #not marion
            self.addunseen(chat)
        # disconnect from server
        db.close()

    def createUser(self,username,role,password=""):
        db=self.getConnection()

        cursor = db.cursor()
        sql = "INSERT INTO people( \
           `access`,`name` ,`password`) \
           VALUES (%d, '%s', '%s')" % \
           (role, username, password)

        cursor.execute(sql)
        db.commit()
        userID=cursor.lastrowid
        # disconnect from server
        db.close()
        chatID=self.createChat(userID)
        print("userID,chatID",userID,chatID)
        return userID,chatID

    def createChat(self,userID):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "INSERT INTO chats( \
           `userid`) \
           VALUES (%d)" % \
           (userID)

        cursor.execute(sql)
        db.commit()
        chatID=cursor.lastrowid
        # disconnect from server
        db.close()
        return chatID

    def ismarionOnline(self):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT value FROM globals WHERE name='marionlastcheck'"
        cursor.execute(sql)
        results = cursor.fetchone()
        db.close()
        #lastmarion = datetime.datetime.fromtimestamp(results["ismariononline"])
        lastmarion=int(results["value"])
        now=time.time()

        margin=5*60

        if (lastmarion+margin)>now:
            return True
        else:
            return False

    def setMarionStatus(self):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "UPDATE globals SET value = '"+str(int(time.time()))+ "' WHERE name='marionlastcheck'"

        cursor.execute(sql)
        db.commit()
        # disconnect from server
        db.close()

    def getLastTimeNotified(self):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "SELECT value FROM globals WHERE name='lasttimenotified'"
        cursor.execute(sql)
        results = cursor.fetchone()
        db.close()
        #lastmarion = datetime.datetime.fromtimestamp(results["ismariononline"])
        lastmarion=int(results["value"])
        return lastmarion

    def updateGlobal(self,name,value):
        db=self.getConnection()
        cursor = db.cursor()
        sql = "UPDATE globals SET value = '"+str(value)+ "' WHERE name='"+name+"'"

        cursor.execute(sql)
        db.commit()
        # disconnect from server
        db.close()

    def getAllConversations(self):
        chats=self.getChats()
        print("chats",len(chats))
        nummessages=0
        conversations=[]

        blacklisted=["http"]

        for chat in chats:
            msgs=self.getMessages(chat["id"],False)

            conversation=[]
            speaking=1 #marion

            for msg in msgs:
                block=[]
                texto=msg["text"]
                block.append("")
                if msg["from"]==1:
                    block.append("MARION:")
                else:
                    block.append("LOCUTOR:")

                block.append(texto)
                nummessages+=1
                shouldpass=True
                for b in blacklisted:
                    if b.upper() in texto.upper():
                        shouldpass=False

                if shouldpass:
                    conversation.extend(block)
            conversations.append(conversation)
            #print (conversation)
            #print (msgs)

        print("nummessages",nummessages)
        return conversations
        #print(chats)
        #chatid=
        #self.getMessages(chatid)

    def getAllConversationsOLD(self):
        chats=self.getChats()

        conversations=[]

        for chat in chats:
            msgs=self.getMessages(chat["id"],False)

            conversation=[]
            speaking=1 #marion
            cache=""
            for msg in msgs:
                cache=cache+" "+msg["text"]
                if msg["from"]!=speaking:
                    #print("speaker changed")
                    #speaker changed
                    speaking=msg["from"]

                    conversation.append(cache)

                    cache=""
            conversations.append(conversation)
            #print (conversation)
            #print (msgs)


        return conversations
        #print(chats)
        #chatid=
        #self.getMessages(chatid)

    def getFlatConversations(self):

        conversations=self.getAllConversations()

        #print(len(conversations),"conversations")

        msgs=[]

        for conv in conversations:
            for msg in conv:
                msgs.append(msg)

        #print(len(msgs),"messages")
        msgsClean=[]
        skip=0
        for texto in msgs:
            if "marion_" in texto:
                skip=2
            if skip>0:
                skip-=1
            else:
                msgsClean.append(texto)
        return msgsClean
