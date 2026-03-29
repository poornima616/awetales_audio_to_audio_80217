import tkinter as tk
from tkinter import filedialog, ttk
import whisper
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pygame
import noisereduce as nr
from scipy.io import wavfile
import numpy as np
model = whisper.load_model("base")
translator = Translator()
pygame.mixer.init()
def reduce_noise(input_path, output_path):
    rate, data = wavfile.read(input_path)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write(output_path, rate, reduced_noise.astype(np.int16))
def process_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if file_path == "":
        return
    clean_audio = "clean.wav"
    try:
        reduce_noise(file_path, clean_audio)
        audio_path = clean_audio
    except:
        audio_path = file_path
    result = model.transcribe(audio_path)
    text = result["text"]
    asr_output.delete("1.0", tk.END)
    asr_output.insert(tk.END, text)
    lang_name = lang_box.get()
    lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(lang_name)]
    translated = translator.translate(text, dest=lang_code)
    trans_output.delete("1.0", tk.END)
    trans_output.insert(tk.END, translated.text)
    tts = gTTS(text=translated.text, lang=lang_code)
    tts.save("output.mp3")
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
def save_audio():
    text = trans_output.get("1.0", tk.END).strip()
    if text == "":
        return
    lang_name = lang_box.get()
    lang_code = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(lang_name)]
    tts = gTTS(text=text, lang=lang_code)
    tts.save("dubbed_output.mp3")
    print("Audio saved as dubbed_output.mp3")
root = tk.Tk()
root.title("Story Telling App (AI Powered)")
root.geometry("700x600")
tk.Label(root, text="AI Story Telling App", font=("Arial", 18, "bold")).pack(pady=10)
btn = tk.Button(root, text="Upload Audio & Generate Story", command=process_audio)
btn.pack(pady=10)
save_btn = tk.Button(root, text=" Save Output Audio", command=save_audio)
save_btn.pack(pady=5)
tk.Label(root, text="Select Output Language").pack()
languages = list(LANGUAGES.values())
lang_box = ttk.Combobox(root, values=languages)
lang_box.set("hindi")
lang_box.pack(pady=5)
tk.Label(root, text="Speech to Text").pack()
asr_output = tk.Text(root, height=6, width=70)
asr_output.pack(pady=5)
tk.Label(root, text="Translated Story").pack()
trans_output = tk.Text(root, height=6, width=70)
trans_output.pack(pady=5)
root.mainloop()