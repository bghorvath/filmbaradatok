import os
import time
import json
import gc

import ffmpeg
import whisper

from preprocessing.notify import notify
from preprocessing.convert_audio import convert_audio

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
    


def main():
    audio_dir = "data/audio"
    text_dir = "data/speech_recognition"
    speech_recognition = SpeechRecognition("large-v2")
    audio_list = []
    audio_length_dict = {}
    for audio_file in os.listdir(audio_dir):
        if audio_file.endswith(".mp3") and not os.path.exists(os.path.join(text_dir, f"{audio_file[:-4]}.json")):
            audio_length = ffmpeg.probe(os.path.join(audio_dir, audio_file)).get("format", {}).get("duration")
            audio_length = int(float(audio_length))
            audio_length_dict[audio_file] = audio_length
            if audio_length < 16000:
                audio_list.append(audio_file)
            else:
                for i in range(audio_length//16000+1):
                    convert_audio(
                        os.path.join(audio_dir, audio_file),
                        os.path.join(audio_dir, f"{audio_file[:-4]}_{i}.mp3"),
                        i * 16000,
                        (i + 1) * 16000,
                    )
                    audio_list.append(f"{audio_file[:-4]}_{i}.mp3")
    
    for i, audio_file in enumerate(audio_list):
        gc.collect()
        current_time = time.strftime("%H:%M", time.localtime())
        eta = time.strftime("%H:%M", time.localtime(time.time() + audio_length_dict[audio_file]/2))
        notify(f"{current_time} | STARTED transcribing {audio_file} | {i+1}/{len(audio_list)} | ETA: {eta}")
        start = time.time()
        result = speech_recognition.transcribe(os.path.join(audio_dir, audio_file))
        end = time.time()
        current_time = time.strftime("%H:%M", time.localtime())
        notify(f"{current_time} | FINISHED transcribing {audio_file} | {i+1}/{len(audio_list)} | TOOK {int((end-start)//3600)}h {int(((end-start)%3600)//60)}m")
        with open(os.path.join(text_dir, f"{audio_file[:-4]}.json"), "w") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        if "_" in audio_file:
            os.remove(os.path.join(audio_dir, audio_file))

if __name__ == "__main__":
    main()
