# hmi-backend

# Install
- create a python environment, then run `pip install -r requirements.txt`
- create `video`, `audio`, `model` folders in project folder
- download [ffmpeg](https://ffmpeg.org/download.html), put `ffmpeg.exe` in project folder
- download `vosk-model-en-us-0.21` model from [vosk](https://alphacephei.com/vosk/models), then `Extract here` under `model` folder

# Operation
- Run uvicorn: `uvicorn main:app --reload`

# Try API at swagger doc
- http://127.0.0.1:8000/docs#/
