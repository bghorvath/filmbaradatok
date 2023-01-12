import subprocess

def convert_audio(input_path: str, output_path: str) -> None:
    """Convert audio file to WAV file.
    Args:
        file_path (str): Path to audio file.
    Returns:
        str: Path to converted audio file.
    """
    sample_rate = 16000
    sample_start_min = 0
    sample_end_min = 180
    subprocess.call(
        [
            "ffmpeg",
            "-y", # overwrite output file if it exists
            "-i", # input file
            input_path,
            "-ac", # number of audio channels
            "1", # mono
            "-ar", # audio sampling rate
            str(sample_rate),
            "-ss", # sample start time
            str(sample_start_min * 60),
            "-to", # sample end time
            str(sample_end_min * 60),
            output_path, # output file
        ]
    )
