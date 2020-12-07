import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from main import *
import time


load_weights = tl.files.load_npz(name='saved/model_e28.npz')
tl.files.assign_weights(load_weights, model_)

#model = tl.files.load_npz(path='saved', name='model_15-06-2020.npz')


def respond(input):
    sentence = inference(input, 3)
    response=' '.join(sentence)
    return response

while True:
    userInput=input("user# ")
    time.sleep(0.5)
    response=respond(userInput)
    print("bot# ",response)
