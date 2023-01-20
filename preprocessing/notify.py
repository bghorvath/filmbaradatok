import os
import json
import requests

def notify(message: str) -> None:
    """
    Send a message to a Telegram chat.

    Args:
        message (str): Message to send.
    """
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if telegram_token is None or chat_id is None:
        raise ValueError("TELEGRAM_TOKEN or TELEGRAM_CHAT_ID environment variables are not set")

    telegram_url = f"https://api.telegram.org/bot{telegram_token}"

    params = {"chat_id": chat_id, "text": message}
    requests.get(telegram_url + "/sendMessage", params=params)
