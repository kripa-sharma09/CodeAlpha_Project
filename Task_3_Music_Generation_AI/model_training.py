import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, BatchNormalization, Activation
from keras.utils import np_utils
import os

# ✅ Ensure model folder exists
if not os.path.exists('model'):
    os.makedirs('model')

# ✅ Load Preprocessed Notes
with open('data/notes.pkl', 'rb') as filepath:
    notes = pickle.load(filepath)

pitchnames = sorted(set(notes))
note_to_int = {note: number for number, note in enumerate(pitchnames)}

sequence_length = 100
network_input = []
network_output = []

for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    network_input.append([note_to_int[char] for char in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)

# ✅ Reshape and Normalize Input
X = np.reshape(network_input, (n_patterns, sequence_length, 1)) / float(len(pitchnames))
y = np_utils.to_categorical(network_output)

# ✅ Define Deep LSTM Model
model = Sequential()
model.add(LSTM(512, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(BatchNormalization())

model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(BatchNormalization())

model.add(LSTM(512))
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(BatchNormalization())

model.add(Dense(len(pitchnames)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

# ✅ Train the Model
model.fit(X, y, epochs=200, batch_size=64)

# ✅ Save the Model
model.save('model/music_model.h5')

print("✅ Model trained and saved successfully at 'model/music_model.h5'")