import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import speech_recognition as sr
import tempfile
import hashlib
import soundfile as sf
import pygame
import streamlit as st
import time
from audio_recorder_streamlit import audio_recorder

# Load environment variables
load_dotenv()

# Initialize Streamlit page configuration
st.set_page_config(page_title="Voice Chat Bot", page_icon="🎤")
st.title("Voice Chat Assistant 🤖")

# Initialize the LLM
@st.cache_resource
def init_llm():
    return ChatGroq(
        api_key=os.getenv('GROQ_API_KEY'),
        model_name="mixtral-8x7b-32768"
    )

llm = init_llm()

# Simple in-memory cache for LLM responses
llm_cache = {}

def get_llm_response(text):
    """
    Retrieves LLM response from cache if available, otherwise calls the LLM.
    """
    cache_key = hashlib.md5(text.encode('utf-8')).hexdigest()

    if cache_key in llm_cache:
        return llm_cache[cache_key]
    else:
        message = HumanMessage(content=text)
        response = llm.invoke([message])
        llm_cache[cache_key] = response.content
        return response.content

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def speech_to_text(audio_data):
    """Converts speech to text using Google Speech Recognition."""
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        st.error("Could not understand the audio")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def text_to_speech(text):
    """Generates speech from text using pyttsx3."""
    import pyttsx3
    
    cache_key = hashlib.md5(text.encode('utf-8')).hexdigest()
    output_path = "response.wav"
    
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()
    
    return output_path

def main():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Audio recording section
    st.subheader("Voice Input")
    audio_bytes = audio_recorder()

    if audio_bytes:
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Convert audio to the format expected by speech_recognition
        audio_data = sr.AudioFile(temp_audio_path)
        with audio_data as source:
            audio = recognizer.record(source)

        # Convert speech to text
        with st.spinner("Transcribing..."):
            transcribed_text = speech_to_text(audio)

        if transcribed_text:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": transcribed_text})
            with st.chat_message("user"):
                st.write(transcribed_text)

            # Get AI response
            with st.spinner("Thinking..."):
                llm_response = get_llm_response(transcribed_text)

            # Add assistant response to chat
            st.session_state.messages.append({"role": "assistant", "content": llm_response})
            with st.chat_message("assistant"):
                st.write(llm_response)

            # Convert response to speech
            with st.spinner("Generating voice response..."):
                audio_file = text_to_speech(llm_response)
                
            # Play audio response
            with open(audio_file, 'rb') as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/wav')
            
            # Cleanup temporary files
            os.remove(temp_audio_path)
            os.remove(audio_file)

    # Add a clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()