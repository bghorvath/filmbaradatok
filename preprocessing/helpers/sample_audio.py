import subprocess

def sample_audio(file_name: str):
    """Sample audio file to 16kHz mono WAV file.

    Args:
        file_path (str): Path to audio file.

    Returns:
        str: Path to sampled audio file.
    """
    file_path = "data/audio/" + str(file_name) + ".mp3"
    sample_rate = 16000
    sample_start_min = 0
    sample_end_min = 60
    sample_path = "preprocessing/speaker_segmentation/" + str(file_name) + "_sampled.wav"
    subprocess.call(
        [
            "ffmpeg",
            "-y", # overwrite output file if it exists
            "-i", # input file
            file_path,
            "-ac", # number of audio channels
            "1", # mono
            "-ar", # audio sampling rate
            str(sample_rate),
            "-ss", # sample start time
            str(sample_start_min * 60),
            "-to", # sample end time
            str(sample_end_min * 60),
            sample_path, # output file
        ]
    )

if __name__ == "__main__":
    sample_audio(240)