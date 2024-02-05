import random
import nltk
import json
import tkinter as tk
from tkinter import scrolledtext
from tkinter import simpledialog
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers import Dense, Activation, Dropout
from keras.models import load_model
import numpy as np
from spellchecker import SpellChecker
import pickle

# Initialize WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents from JSON file
intents = json.loads(open('intents.json').read())
print(intents)
# Initialize lists for words, classes, and documents
word_list = []
classes = []
docs = []
ignore = ['?', ',', '.', '!']

# Process intents and tokenize words
for intent in intents['intents']:
    for pattern in intent['patterns']:
        words = nltk.word_tokenize(pattern)
        word_list.extend(words)
        docs.append((words, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and clean word_list
word_list = [lemmatizer.lemmatize(word.lower()) for word in word_list if word not in ignore]
word_list = sorted(set(word_list))
classes = sorted(set(classes))

# Save word_list and classes to pickle files
with open('word_list.pkl', 'wb') as word_list_file:
    pickle.dump(word_list, word_list_file)

with open('classes.pkl', 'wb') as classes_file:
    pickle.dump(classes, classes_file)

train_data = []
output_data = [0] * len(classes)

# Create training data
for doc in docs:
    bag = []
    word_pattern = doc[0]
    word_pattern = [lemmatizer.lemmatize(word.lower()) for word in word_pattern]
    for word in word_list:
        bag.append(1) if word in word_pattern else bag.append(0)
    output_row = list(output_data)
    output_row[classes.index(doc[1])] = 1
    train_data.append([bag, output_row])

# Shuffle the training data
random.shuffle(train_data)

# Split the training data into inputs and outputs
train_x = [data[0] for data in train_data]
train_y = [data[1] for data in train_data]

# Create and compile the neural network model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.0001, decay=1e-6, momentum=True, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
history = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

# Save the trained model
model.save('chatbot.h5')

print('Model saved successfully!')
