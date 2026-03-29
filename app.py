import streamlit as st
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
model = whisper.load_model("base")
translator = Translator()
st.set_page_config(page_title="AI Dubbing App", layout="centered")
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
st.title("AI Audio/Video Dubbing App")
uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
languages = list(LANGUAGES.values())
lang_name = st.selectbox("Select Output Language", languages, index=languages.index("hindi"))
if uploaded_file:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())
    if st.button("Process Video"):
        st.info("Processing... Please wait ....")
        video = VideoFileClip("temp_video.mp4")
        video.audio.write_audiofile("temp_audio.wav")
        result = model.transcribe("temp_audio.wav")
        text = result["text"]
        st.subheader("Extracted Text")
        st.text_area("", text, height=150)
        lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(lang_name)]
        translated = translator.translate(text, dest=lang_code)
        st.subheader("Translated Text")
        st.text_area("", translated.text, height=150)
        tts = gTTS(text=translated.text, lang=lang_code)
        tts.save("output.mp3")
        st.subheader("Generated Audio")
        st.audio("output.mp3")
        audio = AudioFileClip("output.mp3")
        final_video = video.set_audio(audio)
        final_video.write_videofile("dubbed_video.mp4")
        st.subheader("Download Dubbed Video")
        with open("dubbed_video.mp4", "rb") as file:
            st.download_button("Download Video", file, file_name="dubbed_video.mp4")