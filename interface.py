import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from main import *
import time

load_weights = tl.files.load_npz(name='saved/model_16-06-2020_2.npz')
tl.files.assign_weights(load_weights, model_)

def answer(input):
    sentence = inference(input, 3)
    response=' '.join(sentence)
    return response
