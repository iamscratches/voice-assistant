# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 21:50:55 2020

@author: subhankar
"""

import nltk
#nltk.download()
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
# import os.path
from os import path

stemmer = LancasterStemmer()
tf.compat.v1.reset_default_graph()


with open("models\\intents.json") as file:
    data = json.load(file)
    
    

try:
    with open("models\\data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
    
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    
    for intent in data['intents']:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent['tag'] not in labels:
            labels.append(intent['tag'])
    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))
    
    labels = sorted(labels)
    
    training = []
    output = []
    
    out_empty = [0 for _ in range(len(labels))]
    
    for x, doc in enumerate(docs_x):
        bag = []
        
        wrds = [stemmer.stem(w) for w in doc]
        
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)
        
    training = np.array(training)
    output = np.array(output)
    
    with open("models\\data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation = "softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

if(path.exists("models\\model.tflearn.index")):
    model.load("models\\model.tflearn")
else:
    model.fit(training, output, n_epoch=500, batch_size=8, show_metric=True)
    model.save("models\\model.tflearn")

def __bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
                
    return np.array(bag)

def chat(text):
    results = model.predict([__bag_of_words(text, words)])
    #print(results)
    results_index = np.argmax(results)
    #print(results_index)
    tag = labels[results_index]
    print(tag)
    
    if results[0][results_index] > 0.75:        
        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
                
        return tag,random.choice(responses)
    else:
        return "none","I didn't quiet understand you, please try again!!"
        


