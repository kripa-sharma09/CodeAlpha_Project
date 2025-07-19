from music21 import instrument, note, chord, stream
import numpy as np
import pickle
from keras.models import load_model
import random
import os

# ✅ Ensure output folder exists
if not os.path.exists('generated_music'):
    os.makedirs('generated_music')

# ✅ Load the trained model & notes
model = load_model('model/music_model.h5')

with open('data/notes.pkl', 'rb') as filepath:
    notes = pickle.load(filepath)

pitchnames = sorted(set(notes))
note_to_int = {note: number for number, note in enumerate(pitchnames)}
int_to_note = {number: note for number, note in enumerate(pitchnames)}

# ✅ Temperature-based Sampling Function
def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-8) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds.flatten(), 1)
    return np.argmax(probas)

# ✅ Prepare random seed input
start = random.randint(0, len(notes) - 100)
pattern = [note_to_int[note] for note in notes[start:start + 100]]

# ✅ Randomize output length between 300 to 600 notes
output_length = random.randint(300, 600)

prediction_output = []

for note_index in range(output_length):
    input_seq = np.reshape(pattern, (1, len(pattern), 1)) / float(len(pitchnames))
    prediction = model.predict(input_seq, verbose=0)
    index = sample(prediction[0], temperature=0.7)  # 🎶 Add creativity with temperature
    result = int_to_note[index]
    prediction_output.append(result)
    pattern.append(index)
    pattern = pattern[1:]

# ✅ Convert output notes to MIDI
offset = 0
output_notes = []

for pattern in prediction_output:
    if ('.' in pattern) or pattern.isdigit():
        notes_in_chord = pattern.split('.')
        chord_notes = [note.Note(int(n)) for n in notes_in_chord]
        new_chord = chord.Chord(chord_notes)
        new_chord.offset = offset
        output_notes.append(new_chord)
    else:
        new_note = note.Note(pattern)
        new_note.offset = offset
        output_notes.append(new_note)
    offset += 0.5

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='generated_music/generated.mid')

print(f"✅ New AI-generated music with temperature sampling saved in 'generated_music/generated.mid' — {output_length} notes generated.")