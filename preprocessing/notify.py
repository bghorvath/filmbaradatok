import os
import json
import requests

def notify(message: str) -> None:
    """
    Send a message to a Telegram chat.

    Args:
        message (str): Message to send.
    """
    with open(os.path.join("data", "misc", "telegram.token"), "r") as f:
        telegram_credentials = json.load(f)

    telegram_token = telegram_credentials["token"]
    chat_id = telegram_credentials["chat_id"]

    telegram_url = f"https://api.telegram.org/bot{telegram_token}"

    params = {"chat_id": chat_id, "text": message}
    requests.get(telegram_url + "/sendMessage", params=params)
