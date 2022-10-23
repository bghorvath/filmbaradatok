# FilmbarAdatok - Transcribing audio of popular Hungarian podcast and transforming into meaningful data

![Filmbarátok logo](https://cloud.bghorvath.dev/wl/?id=H068sV9RRDCKBJ4VfK0vree2RMHvRYgQ&fmode=open)

The project consists of:
- Crawling every main episode of [Filmbarátok podcast](https://filmbaratok.blog.hu)
- Transcription of the crawled audio using OpenAI's [Whisper](https://github.com/openai/whisper) pretrained speech recognition model
- Speaker recognition
- Making the transcriptions searchable (with timestamps)
- Visualizing stats about the episodes, speakers, topics, etc.
- Matching transcriptions with most memorable quotes from crawling Twitter API, and presenting them