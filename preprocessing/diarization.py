import os
import yaml
from pyannote.audio import Pipeline
from preprocessing.get_speakers import get_speakers

class Diarization:
    def __init__(self, file_name: str) -> None:
        self.audio_file_path = os.path.join("data", "audio", file_name)
        with open(os.path.join("data", "misc", "huggingface.token"),"r") as f:
            self.access_token = f.read().strip()
        self.speakers = get_speakers(rss_path=os.path.join("data", "misc", "episodes.rss"))
        self.speaker_embeddings = self.get_speaker_embeddings()
        self.diarization = self.get_diarization()
    
    def get_speaker_embeddings(self):
        pass

    def get_diarization(self):
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=self.access_token)
        diarization = pipeline(self.audio_file_path)
        return [{"start": turn.start, "end": turn.end, "speaker": speaker} for turn, _, speaker in diarization.itertracks()]
