import requests


def send_telegram_message(bot_token: str, chat_id: str, message: str) -> None:
    """
    Telegram bot API. Send message to user

    :param str bot_token:
    :param str chat_id:
    :param str message:
    :return None:
    """
    if bot_token and chat_id:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(response.text)
