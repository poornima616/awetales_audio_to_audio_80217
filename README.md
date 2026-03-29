# awetales_audio_to_audio_80217
** AI Audio/Video Dubbing App**

This project is an AI-powered audio and video dubbing platform that converts speech from a video into another language and generates a dubbed output video.

** Overview**
The application performs the following steps:
- Extracts audio from video input
- Converts speech to text using ASR (Whisper)
- Translates the text into a selected target language
- Generates speech using Text-to-Speech (gTTS)
- Merges translated audio back into the original video

** Features**
- Multi-language translation support
- Automatic speech recognition (ASR)
- Text-to-speech (TTS) audio generation
- Video dubbing with translated audio
- Simple web interface using Streamlit

** Tech Stack**
- Python
- Streamlit
- OpenAI Whisper
- Google Translate API (googletrans)
- gTTS (Google Text-to-Speech)
- MoviePy
- FFmpeg

** Installation**

Install required dependencies:

```bash
pip install -r requirements.txt
```
** Running the Application**
python -m streamlit run app.py
Then open the browser at: http://localhost:8501

**Project Structure**
app.py              # Main Streamlit web application  
samp.py             # Core video processing logic  
story_app.py        # Additional audio processing module  
requirements.txt    # Dependencies

**How It Works**
Upload a video file
Select target language
Click "Process Video
View extracted and translated text
Download dubbed video

**Use Cases**
Media localization
Content creation
Accessibility for different languages
Educational tools

**Future Improvements**
Real speaker diarization
Voice cloning
Lip-sync alignment
Faster processing using GPU
