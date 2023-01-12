from typing import Iterable
import re
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

def parse_rss(xml_path: str) -> list[dict]:
    """
    Parse RSS file for episode data.

    Args:
        xml_path (str): Path to RSS file.

    Returns:
        list[dict]: List of episode data.
    """
    with open(xml_path, "r") as file:
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
