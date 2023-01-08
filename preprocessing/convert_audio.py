import os
import subprocess

def convert_audio(file_name: str):
    """Convert audio file to WAV file.
    Args:
        file_path (str): Path to audio file.
    Returns:
        str: Path to converted audio file.
    """
    file_path = "data/audio/" + str(file_name) + ".mp3"
    output_file_path = "data/audio/" + str(file_name) + ".wav"
    sample_rate = 16000
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
            output_file_path, # output file
        ]
    )

if __name__ == "__main__":
    for file_name in os.listdir("data/audio"):
        if file_name.endswith(".mp3"):
            convert_audio(file_name[:-4])
