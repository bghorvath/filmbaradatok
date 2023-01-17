import os
import time
import json
import whisper
from preprocessing.notify import notify

class SpeechRecognition:
    def __init__(self, model_size: str):
        try:
            self.model = whisper.load_model(model_size)
        except:
            raise Exception("Model not found.")

    def transcribe(self, audio_path: str) -> list[dict]:
        transcript = self.model.transcribe(audio_path)
        return [
            {
                "start": x["start"],
                "end": x["end"],
                "text": x["text"],
            }
            for x in transcript["segments"]
        ]

if __name__ == "__main__":
    audio_dir = "data/audio"
    text_dir = "data/speech_recognition"
    speech_recognition = SpeechRecognition("large-v2")
    audio_list = [f for f in os.listdir(audio_dir) if f.endswith(".mp3") and not os.path.exists(os.path.join(text_dir, f"{f[:-4]}_transcript.json"))]
    for i, f in enumerate(audio_list):
        start = time.time()
        audio_path = os.path.join(audio_dir, f)
        result = speech_recognition.transcribe(audio_path)
        with open(os.path.join(text_dir, f"{f[:-4]}_transcript.json"), "w") as f:
            json.dump(result, f, indent=4)
        end = time.time()
        notify(f"Job {i+1}/{len(audio_list)} done in {(end-start)//3600}h {(end-start)//60}m: transcribed {f}")
