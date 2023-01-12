from typing import Iterable
import requests
from tqdm import tqdm
from preprocessing.rss_parser import parse_rss

def get_urls(eps: list[dict], main_only: bool) -> Iterable[tuple[str, str]]:
    for ep in eps:
        filename = ep.get("filename")
        url = ep.get("download")
        if not main_only:
            yield url, filename
        if isinstance(filename, int):
            yield url, filename

def scrape_episode(url: str, filename: str) ->  None:
    r = requests.get(url)
    with open(f"data/audio/{filename}.mp3", "wb") as file:
        file.write(r.content)

def scrape_all_episodes(rss_path = "../data/misc/episodes.rss"):
    episodes_rss = parse_rss(rss_path)
    urls = get_urls(episodes_rss, main_only=True)
    for url, filename in tqdm(urls):
        scrape_episode(url, filename)

if __name__ == "__main__":
    scrape_all_episodes()
