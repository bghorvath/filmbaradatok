# filmbarAdatok - Diarized transcription and insight extraction of podcast audio data

<p align="center">
  <img src="https://cloud.bghorvath.dev/wl/?id=H068sV9RRDCKBJ4VfK0vree2RMHvRYgQ&fmode=open" />
</p>

## About

This is a hobby project that aims to scrape, transcribe, diarize, and analyze a popular Hungarian podcast. The main goals are to archive the spoken content of the podcast, make it searchable, and extract interesting insights from the data about the podcast, its speakers, and the topics they talk about.

The project is open source, and the data will be accessible by anyone over a web app.

Despite the fact that the podcast is in Hungarian, every model used in the project are multilingual, so the project can be easily adapted to other podcasts in other languages.

The project consists of:
- Scraping the 240+ main episodes of [Filmbarátok podcast](https://filmbaratok.blog.hu)
- Transcribing the 780+ hours of audio data using OpenAI's [Whisper](https://github.com/openai/whisper) pretrained speech recognition model
- Speaker diarization using [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- Creating the transcripts speaker-aware by matching the speaker diarization results with the transcriptions
- Extensive data analysis about the episodes, speakers, topics, and so on
- Developing a web app with Elasticsearch for searching the transcripts, and a landing page with the data insights
- Matching transcriptions with quotes from Twitter API in search for the most memorable ones (if possible)

## Speech recognition

Speech recognition is the process of converting spoken words into text. The speech recognition was done using OpenAI's [Whisper](https://github.com/openai/whisper).

Whisper is a recently released, transformer-based, pretrained speech recognition model. It offers state-of-the-art performance for a variety of less common languages, including Hungarian. The model's ability to transcribe speech in Hungarian so well made this project possible.

All the computations were done on an RTX 3060 GPU. Transcription with the large-v2 model was 2x real time, which means that it took around 390 hours to transcribe the 780 hours of audio data.

## Speaker diarization

Speaker diarization is the process of identifying speakers in an audio recording, it basically answers the question "who spoke when".

It is a crucial step in the project, as it allows us to create speaker-aware transcripts. The speaker diarization is done using the [pyannote.audio](https://github.com/pyannote/pyannote-audio) framework, which utilizes a pretrained speaker segmentation model (detecting changes in the speaker), [speechbrain](https://huggingface.co/speechbrain/spkrec-xvect-voxceleb) speaker embedding model (extracting characteristics of speakers from audio), and an agglomerative hierarchical clustering algorithm (grouping speakers with similar characteristics).

## Disclaimer

- This project is not affiliated with the podcast in any way. The podcast is not aware of this project, and the data is not used for any commercial purposes. The data is not monetized in any way, and the project is not funded by any third party.
- The project is still in progress, and the data is not yet available.
- The quality of the transcriptions is limited by the speech recognition model. While the model used is state-of-the-art for Hungarian, its word error rate is still around [17% on average](https://cdn.openai.com/papers/whisper.pdf), which means that the transcriptions are far from perfect.
- The speaker recognition model also makes mistakes, especially with overlapping speech and occasional voice pitch changes, but is quite accurate on longer segments of speech.
