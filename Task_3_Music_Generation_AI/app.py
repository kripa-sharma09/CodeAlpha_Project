import streamlit as st
from pydub import AudioSegment
import os
import pygame

st.set_page_config(page_title="🎵 AI Music Generator", page_icon="🎶")
st.markdown("""
    <style>
    .stApp {
        background-color: #FAF3E0;  /* Soft cream color */
        color: #2C2C2C;
        font-family: 'Poppins', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p {
        color: #2C2C2C;
    }
    .stButton>button {
        background-color: #FF7E5F;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        box-shadow: 0px 0px 15px #FFB88C;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF9671;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎶 AI Music Generator — Powered by Kripa</h1>", unsafe_allow_html=True)

st.sidebar.title("🎨 Settings")
theme = st.sidebar.selectbox("Choose Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("<style>.stApp {background-color: #2C2C2C; color: white;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp {background-color: #F7E7CE; color: #2C2C2C;}</style>", unsafe_allow_html=True)

st.write("💬 Click below to generate a new music piece:")
if st.button("🎵 Generate Music"):
    st.success("✅ Music Generated! Find it in the 'generated_music/' folder.")
    # You can optionally embed audio player here if converted to WAV

if st.button("🔽 Download Generated MIDI"):
    with open('generated_music/generated.mid', 'rb') as f:
        st.download_button('Download MIDI', f, file_name='generated_music.mid')


def play_midi(file_path):
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples (experiment to get right sound)
    
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Example usage:
play_midi('generated_music/generated.mid')