import io
import os
import streamlit as st
from faster_whisper import WhisperModel
import ollama
from gtts import gTTS

st.set_page_config(page_title="Hybrid Voice/Text Chatbot", layout="centered")
st.title("🤖 Interactive Hybrid Chatbot")

# 1. Initialize Chat History & Input Keys
if "messages" not in st.session_state:
    st.session_state.messages = []

# Using a session state key to track processed audio files
if "processed_audio_key" not in st.session_state:
    st.session_state.processed_audio_key = 0

@st.cache_resource
def load_whisper_model():
    return WhisperModel("base", device="cpu", compute_type="int8")

whisper_model = load_whisper_model()

# 2. Helper Functions
def transcribe_audio_local(audio_file):
    temp_filename = f"temp_audio_{st.session_state.processed_audio_key}.wav"
    with open(temp_filename, "wb") as f:
        f.write(audio_file.read())
        
    segments, _ = whisper_model.transcribe(temp_filename, beam_size=5)
    text = "".join([segment.text for segment in segments])
    
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
    return text.strip()

def get_local_llm_response(chat_history):
    response = ollama.chat(model='llama3.2', messages=chat_history)
    return response['message']['content']

def text_to_speech(text_output):
    tts = gTTS(text=text_output, lang='en')
    sound_bytes = io.BytesIO()
    tts.write_to_fp(sound_bytes)
    sound_bytes.seek(0)
    return sound_bytes

# 3. Sidebar Controls
st.sidebar.header("⚙️ Settings")
response_mode = st.sidebar.radio(
    "Preferred Response Format:",
    ["Text Only", "Text + Voice Output"],
    index=1
)

if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# 4. Display Chat History First (Clean Rendering)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. Dual Input System
st.write("---")
st.subheader("Speak or Type your message:")

# Dynamic key changing prevents st.audio_input from loop-processing the same recording
audio_key = f"voice_input_{st.session_state.processed_audio_key}"
audio_value = st.audio_input("🎤 Record Voice", key=audio_key, label_visibility="collapsed")

text_value = st.chat_input("Type your message here...")

user_input = ""

# Process text first, then voice
if text_value:
    user_input = text_value
elif audio_value:
    # Read the audio only if we haven't processed it yet
    with st.spinner("Transcribing..."):
        user_input = transcribe_audio_local(audio_value)
    # Increment key so the next rerun treats it as a brand-new blank widget
    st.session_state.processed_audio_key += 1

# 6. Process New Message
if user_input:
    # Save & Display User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate & Display Assistant Message
    with st.chat_message("assistant"):
        with st.spinner("Bot is thinking..."):
            bot_reply = get_local_llm_response(st.session_state.messages)
            st.write(bot_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
            if response_mode == "Text + Voice Output":
                speech_output = text_to_speech(bot_reply)
                st.audio(speech_output, format="audio/mp3", autoplay=True)
                
    st.rerun()
