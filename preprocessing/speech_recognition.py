import os
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
    speech_recognition = SpeechRecognition("large")
    for f in os.listdir("data/audio"):
        if f.endswith(".mp3"):
            result = speech_recognition.transcribe(os.path.join("data", "audio", f))
            notify(f"Job done: transcript for {f}")
            with open(os.path.join("data", "text", f"{f[:-4]}_transcript.json"), "w") as f:
                json.dump(result, f, indent=4)
