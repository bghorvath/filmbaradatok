import whisper

def main():
    model = whisper.load_model("large")
    result = model.transcribe("data/audio/194.wav")
    with open("result.txt", "w") as f:
        f.write(result)
