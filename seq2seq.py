"""
import seq2seq
from seq2seq.models import Seq2Seq

model = Seq2Seq(batch_input_shape=(16, 7, 5), hidden_dim=10, output_length=8, output_dim=20, depth=4)
model.compile(loss='mse', optimizer='rmsprop')
"""
#! /usr/bin/python
# -*- coding: utf-8 -*-

#based on https://github.com/tensorlayer/seq2seq-chatbot

import tensorflow as tf
import tensorlayer as tl
import numpy as np
from tensorlayer.cost import cross_entropy_seq, cross_entropy_seq_with_mask
from tqdm import tqdm
from sklearn.utils import shuffle

try:
    deployed=False
    #from data.twitter import data
    from data.marion import data
except:
    from app.botAIapi.marionbotapi.data.twitter import data
    deployed=True
from tensorlayer.models.seq2seq import Seq2seq
from tensorlayer.models.seq2seq_with_attention import Seq2seqLuongAttention
import sys,os


def initial_setup(data_corpus):
    try:
        metadata, idx_q, idx_a = data.load_data(PATH='data/{}/'.format(data_corpus))
    except:
        metadata, idx_q, idx_a = data.load_data(PATH='app/botAIapi/marionbotapi/data/{}/'.format(data_corpus))
    #print(metadata, idx_q, idx_a)
    (trainX, trainY), (testX, testY), (validX, validY) = data.split_dataset(idx_q, idx_a)
    trainX = tl.prepro.remove_pad_sequences(trainX.tolist())
    trainY = tl.prepro.remove_pad_sequences(trainY.tolist())
    testX = tl.prepro.remove_pad_sequences(testX.tolist())
    testY = tl.prepro.remove_pad_sequences(testY.tolist())
    validX = tl.prepro.remove_pad_sequences(validX.tolist())
    validY = tl.prepro.remove_pad_sequences(validY.tolist())
    return metadata, trainX, trainY, testX, testY, validX, validY

def inference(seed, top_n):
    seed=seed.lower()
    try:
        model_.eval()
        seed_id = [word2idx.get(w, unk_id) for w in seed.split(" ")]
        #print("seed_id",seed_id)
        sentence_id = model_(inputs=[[seed_id]], seq_length=decoder_seq_length, start_token=start_id, top_n = top_n)
        #print("sentence_id",sentence_id)
        #print("#####")
        #print("")
        sentence = []
        for w_id in sentence_id[0]:
            w = idx2word[w_id]
            if w == 'end_id':
                break
            sentence = sentence + [w]
        return sentence
    except:
        return False

#if __name__ == "__main__":
data_corpus = "marion"

#data preprocessing
metadata, trainX, trainY, testX, testY, validX, validY = initial_setup(data_corpus)

# Parameters
src_len = len(trainX)
tgt_len = len(trainY)

assert src_len == tgt_len

batch_size = 32
n_step = src_len // batch_size
src_vocab_size = len(metadata['idx2w']) # 8002 (0~8001)
emb_dim = 1024

word2idx = metadata['w2idx']   # dict  word 2 index
idx2word = metadata['idx2w']   # list index 2 word

unk_id = word2idx['unk']   # 1
pad_id = word2idx['_']     # 0

start_id = src_vocab_size  # 8002
end_id = src_vocab_size + 1  # 8003

word2idx.update({'start_id': start_id})
word2idx.update({'end_id': end_id})
idx2word = idx2word + ['start_id', 'end_id']

src_vocab_size = tgt_vocab_size = src_vocab_size + 2


vocabulary_size = src_vocab_size

num_epochs = 50



decoder_seq_length = 20
model_ = Seq2seq(
    decoder_seq_length = decoder_seq_length,
    cell_enc=tf.keras.layers.GRUCell,
    cell_dec=tf.keras.layers.GRUCell,
    n_layer=3,
    #n_layer=4,
    n_units=256,
    #n_units=700,
    embedding_layer=tl.layers.Embedding(vocabulary_size=vocabulary_size, embedding_size=emb_dim),
    )

"""
model = Seq2seqLuongAttention(
    hidden_size = 6,
    cell = tf.keras.layers.GRUCell,
    embedding_layer=tl.layers.Embedding(vocabulary_size=vocabulary_size, embedding_size=emb_dim),
    method='general',

)
"""
# Uncomment below statements if you have already saved the model

# load_weights = tl.files.load_npz(name='model.npz')
# tl.files.assign_weights(load_weights, model_)
if __name__ == '__main__':

    ##main action

    optimizer = tf.optimizers.Adam(learning_rate=0.001)
    model_.train()

    seeds = ["Ça va ?",
                 "hey ! je serai sûrement à Paris"]
    for epoch in range(num_epochs):
        model_.train()
        trainX, trainY = shuffle(trainX, trainY, random_state=0)
        total_loss, n_iter = 0, 0
        for X, Y in tqdm(tl.iterate.minibatches(inputs=trainX, targets=trainY, batch_size=batch_size, shuffle=False),
                        total=n_step, desc='Epoch[{}/{}]'.format(epoch + 1, num_epochs), leave=False):

            X = tl.prepro.pad_sequences(X)
            _target_seqs = tl.prepro.sequences_add_end_id(Y, end_id=end_id)
            _target_seqs = tl.prepro.pad_sequences(_target_seqs, maxlen=decoder_seq_length)
            _decode_seqs = tl.prepro.sequences_add_start_id(Y, start_id=start_id, remove_last=False)
            _decode_seqs = tl.prepro.pad_sequences(_decode_seqs, maxlen=decoder_seq_length)
            _target_mask = tl.prepro.sequences_get_mask(_target_seqs)

            with tf.GradientTape() as tape:
                ## compute outputs
                output = model_(inputs = [X, _decode_seqs])

                output = tf.reshape(output, [-1, vocabulary_size])
                ## compute loss and update model
                loss = cross_entropy_seq_with_mask(logits=output, target_seqs=_target_seqs, input_mask=_target_mask)

                grad = tape.gradient(loss, model_.all_weights)
                optimizer.apply_gradients(zip(grad, model_.all_weights))

            total_loss += loss
            n_iter += 1

        # printing average loss after every epoch
        print('Epoch [{}/{}]: loss {:.4f}'.format(epoch + 1, num_epochs, total_loss / n_iter))

        for seed in seeds:
            print("Query >", seed)
            top_n = 3
            for i in range(top_n):
                sentence = inference(seed, top_n)
                if sentence:
                    print(" >", ' '.join(sentence))
                else:
                    print("could not create sentence thru inference")
            print("epoch #" ,epoch)
            tl.files.save_npz(model_.all_weights, name='saved/model_e'+str(epoch)+'.npz')

        tl.files.save_npz(model_.all_weights, name='saved/model.npz')
