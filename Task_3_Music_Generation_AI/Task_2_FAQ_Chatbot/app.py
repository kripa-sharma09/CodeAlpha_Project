import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faqs_data import faqs
import pyttsx3

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Prepare Data
questions = [item['question'] for item in faqs]
answers = [item['answer'] for item in faqs]

vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

# Streamlit Page Config + CSS
st.set_page_config(page_title="Git & GitHub FAQ Chatbot 💭", page_icon="❤", layout="centered")
theme = st.sidebar.selectbox("🎨 Choose Theme", ["Light Mode", "Dark Mode"])

if theme == "Dark Mode":
    st.markdown("""
        <style>
        .stApp { background-color: #2C2C2C; color: white; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #F7E7CE; color: #2C2C2C; }
        </style>
    """, unsafe_allow_html=True)

st.markdown("""
     <style>
     .stApp { background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
     .stButton>button { background-color: #ff5e78; color: white; border-radius: 12px; }
     </style>
 """, unsafe_allow_html=True)

# Header with GIF
st.markdown("""
<div style='text-align: center;'>
    <img src='https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG03c21qZDNkdmVkcWZ5NWtqcXhxOHE0eWk1ZGRrOHIyZGQ2dTNpdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/r4Z8zRcmrofHiDMq20/giphy.gif' width='150'>
    <h1>💭Git & GitHub FAQ Chatbot</h1>
    <p>Not your regular bot — I answer with love!💖</p>
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 What Can You Ask Me?"):
    for faq in faqs:
        st.markdown(f"• {faq['question']}")
# st.markdown("""
# <div style='text-align: center;'>
#     <img src='https://media3.giphy.com/media/YondZW6AMjgTEHevF0/giphy.gif' width='100'>
# </div>
# """, unsafe_allow_html=True)

#st.markdown("<h1 style='text-align: center;'>💬 Git & GitHub FAQ Chatbot</h1>", unsafe_allow_html=True)

# Chatbot Logic
user_question = st.text_input("❓ Ask your question:")

if user_question:
    user_vector = vectorizer.transform([user_question])
    similarity = cosine_similarity(user_vector, question_vectors)
    index = similarity.argmax()

    if similarity[0][index] > 0.3:
        st.success(f"💡 Answer: {answers[index]}")

        feedback = st.radio("💬 Was this answer helpful?", ("👍 Yes", "👎 No"))
        if feedback == "👍 Yes":
         st.success("😊 Thank you for your feedback!")
        elif feedback == "👎 No":
         st.info("😕 We'll try to improve.")
        if st.button("Read the Answers"):
           speak_text(answers[index])
    else:
        st.warning("😕 Sorry, I don't know the answer to that question.")

# Footer
st.markdown("""
<div style='text-align: center;'>
    <p>❤Empowering answers — because knowledge is for everyone💫 </p>
</div>
""", unsafe_allow_html=True)