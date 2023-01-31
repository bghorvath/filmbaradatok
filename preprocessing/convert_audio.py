import subprocess

def convert_audio(input_path: str, output_path: str, sample_start_s: int, sample_end_s: int) -> None:
    """Convert audio file to WAV file.
    Args:
        file_path (str): Path to audio file.
    Returns:
        str: Path to converted audio file.
    """
    subprocess.call(
        [
            "ffmpeg",
            "-y", # overwrite output file if it exists
            "-i", # input file
            input_path,
            "-ac", # number of audio channels
            "1", # mono
            "-ar", # audio sampling rate
            "16000",
            "-ss", # sample start time
            str(sample_start_s),
            "-to", # sample end time
            str(sample_end_s),
            output_path, # output file
        ]
    )
