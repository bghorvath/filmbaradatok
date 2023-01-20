import re
from bs4 import BeautifulSoup as bs

class RSSParser:
    def __init__(self, rss_path: str) -> None:
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

    def get_topics(self, filename: int) -> list[dict]:
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
        matched_topics = search.group(1).strip() if search else None

        if filename == 20:
            matched_topics = "Gengszterkorzó - Boardwalk Empire 1:44\nDr. House 13:40\nAmerican Horror Story 29:55\nJeremiah 42:21\nJericho 55:35\nHazudj, ha tudsz (Lie to me) 1:09:51\nSpartacus - 1:21:15\nTerminator - Sarah Connor krónikái 1:33:05"
        
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
