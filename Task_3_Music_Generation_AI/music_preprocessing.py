from music21 import converter, instrument, note, chord
import glob
import pickle

def get_notes(data_path='data/'):
    notes = []
    for file in glob.glob(f"{data_path}/*.mid"):
        midi = converter.parse(file)
        parts = instrument.partitionByInstrument(midi)
        notes_to_parse = parts.parts[0].recurse() if parts else midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    with open('data/notes.pkl', 'wb') as filepath:
        pickle.dump(notes, filepath)
    return notes

if _name_ == "_main_":
    get_notes() 