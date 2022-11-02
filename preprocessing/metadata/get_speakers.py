import re
import ffmpeg
from preprocessing.web.crawler import parse_rss


def get_metadata_artists(file: str) -> list:
    """Get the artists from the file name"""
    artists = ffmpeg.probe(file).get("format", {}).get("tags",{}).get("artist")
    if artists:
        return [x.strip() for x in artists.split(",")]
    return []


def get_speaker_dict() -> dict:
    """Get the speaker dictionary"""
    eps = parse_rss("preprocessing/web/episodes.rss")
    data_path = "data/audio"

    speaker_pattern = re.compile(r"Beszélgetnek:(.+?)\n")

    speaker_dict = {}
    for episode in eps:
        if not isinstance(episode.get("filename"), int):
            continue
        filename = episode.get("filename")
        desc = episode.get("description")
        speaker_search = re.search(speaker_pattern, desc+"\n")
        if speaker_search:
            speakers = speaker_search.group(1).lower()
            speakers = re.sub(r"[áéíóöőúüű]", lambda m: m.group(0).replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ö", "o").replace("ő", "o").replace("ú", "u").replace("ü", "u").replace("ű", "u"), speakers)
            speakers = speakers.split(",")
            speakers = [s.strip() for s in speakers]
        else:
            speakers = get_metadata_artists(f"{data_path}/{filename}.mp3")
        if len(speakers) > 1:
            speaker_dict[filename] = speakers
        else:
            speaker_dict[filename] = []
    return speaker_dict
