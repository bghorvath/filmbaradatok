from typing import Iterable
import re
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

class RSSParser:
    def __init__(self, rss_path) -> None:
        rss_path = rss_path
        rss = self.parse_rss(rss_path)
        self.episode_dict = self.get_ep_dict(rss)
    
    @staticmethod
    def parse_rss(rss_path: str) -> list[dict]:
        """
        Parse RSS file for episode data.

        Args:
            xml_path (str): Path to RSS file.

        Returns:
            list[dict]: List of episode data.
        """
        with open(rss_path, "r") as file:
            content = file.readlines()
            content = "".join(content)
            bs_content = bs(content, "lxml")

        items = bs_content.find("channel").find_all("item")

        eps = []
        for item in items:
            title = item.find("title").text
            pubdate = item.find("pubdate").text
            description = item.find("description").text
            link = item.find("link").text
            download = item.find("enclosure").get("url")
            epno = re.search(r"#\d+", title)
            if epno:
                filename = int(epno.group(0)[1:])
            else:
                filename = title.replace("Filmbarátok", "fb")
                filename = filename.lower().strip()
                filename = re.sub(r"[áéíóöőúüű]", lambda m: m.group(0).replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ö", "o").replace("ő", "o").replace("ú", "u").replace("ü", "u").replace("ű", "u"), filename)
                filename = re.sub(r"[^a-z0-9 ]", "", filename)
                filename = re.sub(r"\s+", "_", filename)

            eps.append({"title": title, "filename":filename, "pubdate": pubdate, "description": description, "link": link, "download": download})

        return eps
    
    @staticmethod
    def get_ep_dict(parsed_rss: list) -> dict[str, dict]:
        ep_dict = {}
        for ep in parsed_rss:
            if type(ep["filename"]) != int:
                continue
            ep_dict[ep["filename"]] = {k: v for k, v in ep.items() if k != "filename"}
        return ep_dict

    def get_topics(self, filename: int) -> list[(str, str)]:
        """
        Get topics from episode description.

        Returns:
            list[(str, str)]: List of topics and timestamps.
        """
        ep = self.episode_dict.get(filename)
        
        if ep is None:
            return []

        pattern = re.compile(r"Téma:?(.{4,}?)(?=\n\n|$)", re.DOTALL)

        search = pattern.search(ep["description"])
        parsed_desc = search.group(1).strip() if search else None

        if filename == 20:
            parsed_desc = "Gengszterkorzó - Boardwalk Empire 1:44\nDr. House 13:40\nAmerican Horror Story 29:55\nJeremiah 42:21\nJericho 55:35\nHazudj, ha tudsz (Lie to me) 1:09:51\nSpartacus - 1:21:15\nTerminator - Sarah Connor krónikái 1:33:05"
        
        if parsed_desc is None:
            return []

        parsed_desc_list = parsed_desc.split("\n")
        desc_timestamp = []
        for desc in parsed_desc_list:
            desc = re.sub(r"^[^a-zA-Z0-9]+", "", desc)
            timestamp = re.search(r"\((?:\d+:?)+\)" , desc)
            if timestamp is not None:
                desc = desc.replace(timestamp.group(0), "")
                timestamp = timestamp.group(0).replace("(", "").replace(")", "")
            desc = desc.lower()
            desc = re.sub(r"[^a-zíéáóöőúüű0-9 ]", " ", desc)
            desc = re.sub(r"\s+", " ", desc)
            desc = desc.replace("spoileres", "")
            desc = desc.strip()
            desc_timestamp.append((desc, timestamp))

        return desc_timestamp
