import os
import requests

def match(topics: list[dict]) -> list[dict]:
    """
    Match topics to IMDb URLs using The Movie Database API.

    Parameters:
        topics (list[dict]): List of topics with timestamps. Format: [{"topic": "topic", "timestamp": "timestamp"}]
    
    Returns:
        list[dict]: List of topics with IMDb URLs. Format: [{"topic": "topic", "timestamp": "timestamp", "imdb_url": "imdb_url"}]
    """
    exclude_topics = {
        "borítókép",
        "sorsolás",
        "villámkérdés",
        "felvezető",
        "zárthelyi",
        "filmév",
        "filmbarátok",
        "oscar",
        "évösszegzés",
    }

    tmdb_api_key = os.environ.get("TMDB_TOKEN")
    if tmdb_api_key is None:
        raise ValueError("TMDB_TOKEN environment variable is not set")
    
    topic_errors = {}

    while True:
        if len(topics) == 0:
            break
        topic_with_timestamp = topics.pop(0)

        topic = topic_with_timestamp["topic"]
        if any(exc in topic for exc in exclude_topics):
            continue
        query = topic.replace(" ", "+")
        tmdb_search = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={query}"
        response = requests.get(tmdb_search)
        if response.status_code == 502:
            topic_errors[topic] = topic_errors.get(topic, 0) + 1
            if topic_errors[topic] < 3:
                topics.append(topic_with_timestamp)
            continue
        if response.status_code != 200:
            continue
        results = response.json()["results"]
        if len(results) == 0:
            continue
        tmdb_id = sorted(results, key=lambda x: x["popularity"], reverse=True)[0]["id"]
        tmdb_lookup = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}"
        response = requests.get(tmdb_lookup)
        if response.status_code == 502:
            topic_errors[topic] = topic_errors.get(topic, 0) + 1
            if topic_errors[topic] < 3:
                topics.append(topic_with_timestamp)
            continue
        if response.status_code != 200:
            continue
        movie = response.json()
        imdb_id = movie.get("imdb_id")
        if imdb_id is None or len(imdb_id) != 9:
            continue
        imdb_url = f"https://www.imdb.com/title/{imdb_id}"
        topic_with_timestamp["imdb_url"] = imdb_url
    
    return topics
