import re
import json
import ffmpeg
from preprocessing.rss_parser import parse_rss


def get_artists_from_metadata(file: str) -> list:
    """Get the artists from the file name"""
    artists = ffmpeg.probe(file).get("format", {}).get("tags",{}).get("artist", "")
    return artists

def get_artists_from_description(episode_rss: dict):
    speaker_pattern = re.compile(r"Beszélgetnek:(.+?)\n")
    desc = episode_rss.get("description")
    speaker_search = re.search(speaker_pattern, desc+"\n")
    if speaker_search:
        return speaker_search.group(1)
    else:
        return None

def get_speakers(rss_path: str, audio_path: str) -> set:
    """Get the speaker dictionary"""
    rss = parse_rss(rss_path)
    filename = audio_path.split("/")[-1].split(".")[0]
    episode_rss = [ep for ep in rss if ep.get("title") == filename]
    speakers = get_artists_from_description(episode_rss[0]) if len(episode_rss) == 1 else None
    if speakers is None:
        speakers = get_artists_from_metadata(audio_path)
    speakers = speakers.split(",")
    speakers = [s.strip().capitalize() for s in speakers]
    if len(speakers) > 1:
        return speakers
    else:
        return []
