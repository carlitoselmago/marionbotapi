from chatterbot import ChatBot
from db import db
from chatterbot.trainers import ListTrainer

db=db()
con=db.getConnection()

chatbot = ChatBot("Marion")


trainer = ListTrainer(chatbot)
conversations=db.getAllConversations()

for conversation in conversations:
    trainer.train(conversation)

#response = chatbot.get_response("Salut")
#print(response)

# The following loop will execute each time the user enters input
print("start conversation:")
while True:
    try:
        user_input = input()

        bot_response = chatbot.get_response(user_input)

        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
