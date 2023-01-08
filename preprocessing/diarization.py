import os
import pickle
from pyannote.audio import Pipeline

def main():
    with open(os.path.join("data", "misc", "huggingface.token"),"r") as f:
        ACCESS_TOKEN = f.read().strip()
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=ACCESS_TOKEN)

    audio_file = "240"
    audio_file_path = os.path.join("data", "audio", audio_file + ".wav")
    
    diarization = pipeline(audio_file_path)
    with open(os.path.join("data", "text", audio_file + ".pkl"), "wb") as f:
        pickle.dump(diarization, f)

if __name__ == "__main__":
    main()
