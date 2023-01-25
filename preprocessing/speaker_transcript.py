from copy import deepcopy
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class SpeakerTranscript:
    def __init__(self, speech, diarization):
        self.speech = speech
        self.diarization = diarization
    
    @staticmethod
    def join_subsentences(speech_data: list[dict]) -> list[dict]:
        """
        Join subsentences into one sentence. WIP.
        """
        dialogues = []
        text = ""
        for dialogue in speech_data:
            new_start = dialogue["start"]
            new_end = dialogue["end"]
            new_text = dialogue["text"]
            new_text = new_text.strip()
            if len(text) > 0:
                new_start = start
                new_text = text + " " + new_text
            if len(new_text) > 0 and new_text[-1] not in {".", "!", "?"}:
                start = new_start
                text = new_text
            else:
                text = ""
                dialogues.append(
                    {
                        "start": new_start,
                        "end": new_end,
                        "text": new_text,
                    }
                )
        return dialogues

    @staticmethod
    def split_into_sentences(dialogues: list[dict]) -> list[dict]:
        """
        Split dialogues into sentences. WIP.
        """
        tokenized_dialogues = []
        for x in dialogues:
            start = x["start"]
            end = x["end"]
            text = x["text"]
            tokenized = sent_tokenize(text)
            if isinstance(tokenized, str):
                tokenized_dialogues.append(x)
            else:
                num_words = len(text.split(" "))
                sent_start = start
                for sent in tokenized:
                    sent_num_words = len(sent.split(" "))
                    sent_end = sent_start + (end - start) * (sent_num_words / num_words)
                    tokenized_dialogues.append(
                        {
                            "start": sent_start,
                            "end": sent_end,
                            "text": sent,
                        }
                    )
                    sent_start = sent_end
        return tokenized_dialogues

    def create_transcript(self) -> list[dict]:
        """
        Create transcript. WIP.
        """
        diarization_data = deepcopy(self.diarization)
        speech_data = self.join_subsentences(self.speech)
        speech_data = self.split_into_sentences(speech_data)
        transcript = []
        speaker = None

        for i, x in enumerate(speech_data):
            new_start = x["start"]
            new_end = x["end"]
            new_text = x["text"]
            new_speaker = None
            segment_speaker_dict = {}

            # filter out audio segments that are past the new start
            diarization_data[:] = (y for y in diarization_data if y["stop"] + 0.2 >= new_start)

            # iterate through audio segments to find speaker
            for audio_segment in diarization_data:
                if new_start <= audio_segment["stop"] + 0.2 and new_end >= audio_segment["start"] - 0.2:
                    speaker_duration = min(audio_segment["stop"], new_end) - max(audio_segment["start"], new_start)
                    segment_speaker = audio_segment["speaker"]
                    segment_speaker_dict[segment_speaker] = segment_speaker_dict.get(segment_speaker, 0) + speaker_duration
                elif new_end + 0.2 < audio_segment["start"]:
                    break
            if len(segment_speaker_dict) > 0:
                max_speaker_duration = max(segment_speaker_dict.values())
                if max_speaker_duration / (new_end - new_start) > 0.5:
                    new_speaker = max(segment_speaker_dict, key=segment_speaker_dict.get)
                else:
                    new_speaker = "unknown"
            else:
                new_speaker = "unknown"

            # first speaker
            if speaker is None:
                speaker_start = new_start
                speaker_end = new_end
                speaker = new_speaker
                speaker_text = ""

            # if old speaker is same as current speaker
            if new_speaker == speaker:
                speaker_text += " " + new_text
                speaker_end = new_end
                if i == len(speech_data) - 1:
                    transcript.append({"start": speaker_start, "end": speaker_end, "speaker": speaker, "text": speaker_text})

            # else: speaker changed, add old speaker to transcript
            else:
                transcript.append({"start": speaker_start, "end": speaker_end, "speaker": speaker, "text": speaker_text})
                speaker_start = new_start
                speaker_end = new_end
                speaker = new_speaker
                speaker_text = new_text
        
        return transcript

    def __call__(self) -> list[dict]:
        return self.create_transcript()
