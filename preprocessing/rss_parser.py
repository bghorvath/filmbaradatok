import re
from datetime import datetime
from bs4 import BeautifulSoup as bs

class RSSParser:
    def __init__(self, rss_path: str) -> None:
        self.rss_path = rss_path
        self.episodes_dict = {}
    
    def parse_rss(self) -> list[dict]:
        """
        Parse RSS file for episode data.

        Args:
            xml_path (str): Path to RSS file.

        Returns:
            list[dict]: List of episode data.
        """
        with open(self.rss_path, "r") as file:
            content = file.readlines()
            content = "".join(content)
            bs_content = bs(content, "lxml")

        items = bs_content.find("channel").find_all("item")

        for item in items:
            title = item.find("title").text
            pubdate = item.find("pubdate").text
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)
            description = item.find("description").text
            link = item.find("link").text
            download = item.find("enclosure").get("url")
            numeric_episode = re.search(r"#\d+", title)
            if numeric_episode:
                filename = int(numeric_episode.group(0)[1:])
            else:
                filename = title.replace("Filmbarátok", "fb")
                filename = filename.lower().strip()
                filename = re.sub(r"[áéíóöőúüű]", lambda m: m.group(0).replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ö", "o").replace("ő", "o").replace("ú", "u").replace("ü", "u").replace("ű", "u"), filename)
                filename = re.sub(r"[^a-z0-9 ]", "", filename)
                filename = re.sub(r"\s+", "_", filename)

            self.episodes_dict[filename] = {"title": title, "pubdate": pubdate, "description": description, "link": link, "download": download}
    
    def __call__(self):
        self.parse_rss()
        return self
    
    @staticmethod
    def get_topics(ep_dict: dict) -> list[dict]:
        """
        Get topics from episode description.

        Returns:
            list[(str, str)]: List of topics and timestamps.
        """
        if ep_dict is None:
            return []

        pattern = re.compile(r"Téma:?(.{4,}?)(?=\n\n|$)", re.DOTALL)

        search = pattern.search(ep_dict["description"])
        matched_topics = search.group(1).strip() if search else None

        if matched_topics is None:
            return []

        matched_topic_list = matched_topics.split("\n")
        desc_timestamp = []
        timestamp_pattern = re.compile(r"\d{1,2}:\d{2}(?::\d{2})?")
        for topic in matched_topic_list:
            timestamp = timestamp_pattern.search(topic)
            if timestamp is not None:
                topic = timestamp_pattern.sub("", topic)
                timestamp = timestamp.group(0)
            topic = topic.lower()
            topic = re.sub(r"[^a-zíéáóöőúüű0-9 ]", " ", topic)
            topic = re.sub(r"\s+", " ", topic)
            topic = topic.replace("spoileres", "")
            topic = topic.strip()
            desc_timestamp.append({"topic": topic, "timestamp": timestamp})

        return desc_timestamp
