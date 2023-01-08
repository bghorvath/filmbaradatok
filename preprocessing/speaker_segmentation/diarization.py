import os
import pickle
from pyannote.audio import Pipeline




def main():
    dir_path = "preprocessing/speaker_segmentation"
    with open(os.path.join(dir_path, "huggingface.token"),"r") as f:
        ACCESS_TOKEN = f.read().strip()
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=ACCESS_TOKEN)

    audio_file = "240_sampled"
    audio_file_path = os.path.join(dir_path, audio_file + ".wav")
    
    diarization = pipeline(audio_file_path)
    with open(os.path.join(dir_path, audio_file + ".pkl"), "wb") as f:
        pickle.dump(diarization, f)

if __name__ == "__main__":
    main()
