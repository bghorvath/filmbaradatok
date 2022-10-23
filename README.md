# FilmbarAdatok - Turning audio data into insights using SOTA NLP methods

![Filmbarátok logo](https://cloud.bghorvath.dev/wl/?id=H068sV9RRDCKBJ4VfK0vree2RMHvRYgQ&fmode=open)

The project consists of:
- Scraping the 241 main episodes of [Filmbarátok podcast](https://filmbaratok.blog.hu) (as of 22/10/2022)
- Transcribing the audio files using OpenAI's [Whisper](https://github.com/openai/whisper) pretrained speech recognition model
- Speaker recognition
- Making the transcriptions searchable (with timestamps)
- Visualizing stats about the episodes, speakers, topics, etc.
- Matching transcriptions with most memorable quotes from crawling Twitter API, and presenting them

Raw audio data is not included in the repository, but can be downloaded from [here](https://cloud.bghorvath.dev/wl/?id=oeO2t9Q9sYGE1sDmME0XGKk9ptd7OYM9&mode=list), or recreated using the crawler script.