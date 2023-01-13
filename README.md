# FilmbarAdatok - Turning audio data into insights using SOTA NLP methods

<p align="center">
  <img src="https://cloud.bghorvath.dev/wl/?id=H068sV9RRDCKBJ4VfK0vree2RMHvRYgQ&fmode=open" />
</p>

The project consists of:
- Scraping the 241 main episodes of [Filmbarátok podcast](https://filmbaratok.blog.hu) (as of 22/10/2022)
- Transcribing the audio files using OpenAI's [Whisper](https://github.com/openai/whisper) pretrained speech recognition model
- Speaker diarization using [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- Making the transcripts searchable
- Visualizing stats about the episodes, speakers, topics, and such
- Matching transcriptions with most memorable quotes from crawling Twitter API
