import os
import time
import json
import whisper
import gc
import ffmpeg
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
    audio_list = []
    for audio_file in os.listdir(audio_dir):
        audio_length = ffmpeg.probe(os.path.join(audio_dir, audio_file)).get("format", {}).get("duration")
        if audio_file.endswith(".mp3") and not os.path.exists(os.path.join(text_dir, f"{audio_file[:-4]}.json")) and float(audio_length) <  16000:
            audio_list.append(audio_file)
    
    for i, audio_file in enumerate(audio_list):
        gc.collect()
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(f"{current_time} |  starting job {i+1}/{len(audio_list)}: transcribing {audio_file}")
        start = time.time()
        audio_path = os.path.join(audio_dir, audio_file)
        result = speech_recognition.transcribe(audio_path)
        end = time.time()
        notify(f"Job {i+1}/{len(audio_list)} done in {int((end-start)//3600)}h {int(((end-start)%3600)//60)}m: transcribed {audio_file}")
        with open(os.path.join(text_dir, f"{audio_file[:-4]}.json"), "w") as f:
            json.dump(result, f, indent=4)
