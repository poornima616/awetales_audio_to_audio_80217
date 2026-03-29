import tkinter as tk
from tkinter import filedialog, ttk
import whisper
from moviepy.editor import VideoFileClip, AudioFileClip
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pygame
from pydub import AudioSegment
import os
model = whisper.load_model("base")
translator = Translator()
pygame.mixer.init()
generated_audio_path = "synced_output.mp3"
def process_video():
    global generated_audio_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4")]
    )
    if file_path == "":
        return
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "Processing...\n")
    audio_path = "temp_audio.wav"
    video = VideoFileClip(file_path)
    video.audio.write_audiofile(audio_path)
    result = model.transcribe(audio_path)
    segments = result["segments"]
    clean_text = ""
    for seg in segments:
        clean_text += seg["text"].strip() + "\n"
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, clean_text)
    lang_name = lang_box.get()
    lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(lang_name)]
    translated_full = translator.translate(clean_text, dest=lang_code)
    trans_box.delete("1.0", tk.END)
    trans_box.insert(tk.END, translated_full.text)
    final_audio = AudioSegment.silent(duration=0)
    for i, seg in enumerate(segments):
        start_time = int(seg["start"] * 1000)
        text_seg = seg["text"].strip()
        translated_seg = translator.translate(text_seg, dest=lang_code).text
        temp_file = f"seg_{i}.mp3"
        tts = gTTS(text=translated_seg, lang=lang_code)
        tts.save(temp_file)
        seg_audio = AudioSegment.from_mp3(temp_file)
        if len(final_audio) < start_time:
            silence = AudioSegment.silent(duration=start_time - len(final_audio))
            final_audio += silence
        final_audio += seg_audio
        os.remove(temp_file)
    generated_audio_path = "synced_output.mp3"
    final_audio.export(generated_audio_path, format="mp3")
    pygame.mixer.music.load(generated_audio_path)
    pygame.mixer.music.play()
def save_audio():
    if os.path.exists(generated_audio_path):
        os.rename(generated_audio_path, "dubbed_output.mp3")
        print("Saved as dubbed_output.mp3")
def create_dubbed_video():
    video_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4")]
    )
    if video_path == "":
        return
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(generated_audio_path)
        final_video = video.set_audio(audio)
        final_video.write_videofile("dubbed_video.mp4")
        print("Dubbed video saved as dubbed_video.mp4")
    except Exception as e:
        print("Error:", e)
root = tk.Tk()
root.title("AI Dubbing App (Timestamp Sync 🔥)")
root.geometry("800x700")
tk.Label(root, text="AI Audio/Video Dubbing App",
         font=("Arial", 18, "bold")).pack(pady=10)
tk.Button(root, text="Upload Video", command=process_video).pack(pady=10)
tk.Button(root, text="Save Output Audio", command=save_audio).pack(pady=5)
tk.Button(root, text="Create Dubbed Video", command=create_dubbed_video).pack(pady=5)
tk.Label(root, text="Select Output Language").pack()
languages = list(LANGUAGES.values())
lang_box = ttk.Combobox(root, values=languages)
lang_box.set("hindi")
lang_box.pack(pady=5)
tk.Label(root, text="Extracted Text").pack()
output_box = tk.Text(root, height=12, width=90)
output_box.pack(pady=5)
tk.Label(root, text="Translated Output").pack()
trans_box = tk.Text(root, height=12, width=90)
trans_box.pack(pady=5)
root.mainloop()