# 🤖 Local Voice & Text Chatbot (Llama 3.2)

A  privacy-first, and hybrid AI chatbot** powered by Meta's **Llama 3.2**. This application runs completely on your local laptop, handles conversational context, and responds via both text and voice—all **without requiring an active internet connection**.

---

## 🌟 Key Features

*   **Hybrid Dual Input:** Seamlessly switch between text typing (`st.chat_input`) and voice recording (`st.audio_input`).
*   **Contextual Memory:** Utilizes Streamlit Session State to retain conversation history for natural multi-turn back-and-forth dialogue.
*   **Local Speech Processing:** Features high-speed offline voice transcription via `Faster-Whisper` and fluid text-to-speech feedback via your operating system's native voice engine (`pyttsx3`).
*   **Format Flexibility:** A sidebar toggle allows you to choose between **Text Only** responses or **Text + Voice Output** with auto-playback.

---

## 🛠️ System Architecture

1. **Capture:** Voice or text is collected through the interactive Streamlit UI.
2. **Speech-to-Text (STT):** Audio buffers are transcribed locally using `Faster-Whisper (base)`.
3. **Reasoning Engine (LLM):** Chat logs are processed locally by `Ollama` running `Llama 3.2 (1B)`.
4. **Text-to-Speech (TTS):** The generated text reply is converted into voice bytes offline using `pyttsx3`.

---

## 📋 Prerequisites & Installation

### 1. Install Python Packages
Ensure you have Python 3.10+ installed on your system. Run the following command to install the required libraries:

```bash
pip install streamlit faster-whisper ollama pyttsx3
```

### 2. Set Up Ollama & Llama 3.2
1. Download and install [Ollama](https://ollama.com) for your operating system.
2. Open your terminal or command prompt and run the following command to download the lightweight model:
   ```bash
   ollama pull llama3.2:1b
   ```
   *(Note: You can swap this with `llama3.2:3b` or `qwen2.5:0.5b` inside the code depending on your computer's hardware specs).*

---

## 🚀 How to Run the App

1. Save your script file as `demo.py` in your project folder.
2. Open your terminal, navigate to the project directory, and launch the server:
   ```bash
   streamlit run demo.py
   ```
3. Your default web browser will automatically open to `http://localhost:8501`.
4. Start chatting by typing your message or clicking the microphone icon to record your voice!

---

## ⚙️ Project File Structure

```text
├── demo.py                 # Core Streamlit app containing UI & local inference loops
├── README.md               # Setup instructions and project details
└── temp_audio_X.wav        # Temporary audio file used for transcription (Auto-deleted)
```

---

## 🛡️ License & Privacy
This project runs entirely on local hardware under open-source compliance terms. No chat history, voice prints, or data payloads are transmitted to external cloud servers, ensuring absolute data privacy.
