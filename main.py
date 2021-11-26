import os
import sys
import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VIDEO_PATH = "video/"
AUDIO_PATH = "audio/"
SetLogLevel(0)

# path to vosk model downloaded from
# https://alphacephei.com/vosk/models
model_path = "model/vosk-model-en-us-0.21"

print(f"Reading your vosk model '{model_path}'...")
model = Model(model_path)
print(f"'{model_path}' model was successfully read")

@app.post("/video")
async def post_video(file: UploadFile = File(...)):
    with open(f'{VIDEO_PATH}/{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video_name = file.filename[:-4]
    audio_filename = "{}{}.wav".format(AUDIO_PATH, video_name)
    if not os.path.exists(audio_filename):
        command2mp3 = f"ffmpeg -i {VIDEO_PATH}{video_name}.mp4 tmp.mp3"
        command2wav = f"ffmpeg -i tmp.mp3 -acodec pcm_s16le -ac 1 {audio_filename}"
        os.system(command2mp3)
        os.system(command2wav)
        os.remove("tmp.mp3")

    if not os.path.exists(model_path):
        print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
        sys.exit()

    # name of the text file to write recognized text
    # text_filename = "../audio/speech_recognition_systems_vosk_with_timestamps.txt"

    if not os.path.exists(audio_filename):
        print(f"File '{audio_filename}' doesn't exist")
        sys.exit()

    print(f"Reading file '{audio_filename}'...")
    wf = wave.open(audio_filename, "rb")
    print(f"'{audio_filename}' file was successfully read")

    # check if audio is mono wav
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit()

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []

    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)
    return results