import os
import time
import json
import gc

import ffmpeg
import whisper

from preprocessing.notify import notify
from preprocessing.convert_audio import convert_audio

class SpeechRecognition:
    def __init__(
        self,
        model_size: str,
        audio_dir: str = "data/audio",
        text_dir: str = "data/text",
        ):
        self.audio_dir = audio_dir
        self.text_dir = text_dir
        
        self.audio_list = [audio_file for audio_file in os.listdir(audio_dir) if audio_file.endswith(".mp3") and not os.path.exists(os.path.join(text_dir, f"{audio_file[:-4]}.json"))]

        try:
            self.model = whisper.load_model(model_size)
        except:
            raise Exception("Model not found.")
    
    def split_audio(self, audio_file: str, audio_parts: int) -> None:
        current_time = time.strftime("%H:%M", time.localtime())
        notify(f"{current_time} | STARTED splitting {audio_file} into {audio_parts} parts")
        for i in range(audio_parts):
            convert_audio(
                os.path.join(self.audio_dir, audio_file),
                os.path.join(self.audio_dir, f"{audio_file[:-4]}_{i}.mp3"),
                i * 16000,
                (i + 1) * 16000,
            )
        current_time = time.strftime("%H:%M", time.localtime())
        notify(f"{current_time} | FINISHED splitting {audio_file} into {audio_parts} parts")
    
    def transcribe(self, audio_file: str) -> list[dict]:
        audio_path = os.path.join(self.audio_dir, audio_file)
        audio_length = ffmpeg.probe(audio_path).get("format", {}).get("duration")
        audio_length = int(float(audio_length))
        if audio_length > 16000:
            transcript = self.model.transcribe(audio_path)
            transcript = [{"start": x["start"], "end": x["end"], "text": x["text"]} for x in transcript["segments"]]
        else:
            audio_parts = audio_length // 16000 + 1
            split_audio(audio_file, audio_parts)
            
            transcript = []
            for i in range(audio_parts):
                audio_file_name = f"{audio_file[:-4]}_{i}.mp3"
                ts = self.model.transcribe(os.path.join(self.audio_dir, audio_file_name))
                ts = [{"start": x["start"] + i * 16000, "end": x["end"] + i * 16000, "text": x["text"]} for x in ts["segments"]]
                transcript += ts

                os.remove(os.path.join(self.audio_dir, audio_file_name))

        return transcript
    
    def __call__(self) -> None:
        for i, audio_file in enumerate(self.audio_list):
            gc.collect()
            
            current_time = time.strftime("%H:%M", time.localtime())
            eta = time.strftime("%H:%M", time.localtime(time.time() + audio_length_dict[audio_file]/2))
            notify(f"{current_time} | STARTED transcribing {audio_file} | {i+1}/{len(self.audio_list)} | ETA: {eta}")
            start = time.time()
            
            result = self.transcribe(audio_file)
            
            end = time.time()
            current_time = time.strftime("%H:%M", time.localtime())
            notify(f"{current_time} | FINISHED transcribing {audio_file} | {i+1}/{len(self.audio_list)} | TOOK {int((end-start)//3600)}h {int(((end-start)%3600)//60)}m")
            
            with open(os.path.join(self.text_dir, f"{audio_file[:-4]}.json"), "w") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    speech_recognition = SpeechRecognition("large-v2")
    speech_recognition()
