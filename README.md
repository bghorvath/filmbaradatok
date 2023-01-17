# FilmbarAdatok - Turning audio data into insights using state-of-the-art NLP models

<p align="center">
  <img src="https://cloud.bghorvath.dev/wl/?id=H068sV9RRDCKBJ4VfK0vree2RMHvRYgQ&fmode=open" />
</p>

The project consists of:
- Scraping the 240+ main episodes of [Filmbarátok podcast](https://filmbaratok.blog.hu)
- Transcribing the 780+ hours of audio data using OpenAI's [Whisper](https://github.com/openai/whisper) pretrained speech recognition model
- Speaker diarization using [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- Creating the transcripts speaker-aware by matching the speaker diarization results with the transcriptions
- Extensive data analysis about the episodes, speakers, topics, and so on
- Developing a web app with Elasticsearch for searching the transcripts, and a landing page with the data insights
- Matching transcriptions with quotes from Twitter API in search for the most memorable ones (if viable)

## Speech recognition

Speech recognition is the process of converting spoken words into text. The speech recognition was done using OpenAI's [Whisper](https://github.com/openai/whisper).
Whisper is a recently released, transformer-based, pretrained speech recognition model. It offers state-of-the-art word error rate performance for a variety of less common languages, including Hungarian. The model's ability to transcribe speech in Hungarian so well made this project possible.

All the computations were done on an RTX 3060 GPU. Transcription with the large-v2 model was 2x real time, which means that it took 390 hours to transcribe the 780 hours of audio data.

## Speaker diarization

Speaker diarization is the process of identifying speakers in an audio recording, it basically answers the question "who spoke when".
It is a crucial step in the project, as it allows us to create speaker-aware transcripts. The speaker diarization is done using the [pyannote.audio](https://github.com/pyannote/pyannote-audio) framework, which utilizes a pretrained speaker segmentation model (detecting changes in the speaker), [speechbrain](https://huggingface.co/speechbrain/spkrec-xvect-voxceleb) speaker embedding model (extracting characteristics of speakers from audio), and an agglomerative hierarchical clustering algorithm (grouping speakers with similar characteristics).
