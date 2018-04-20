import requests
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

bot = ChatBot(
    'Ron Obvious',
    trainer = 'chatterbot.trainers.ChatterBotCorpusTrainer'
)
chatbot.train('chatterbot.corpus.english')

def get_response(request):
   
    
    response =   bot.get_response(request)
    return("Bot: " + str(response))

