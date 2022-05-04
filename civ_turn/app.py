from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
import json
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


class Item(BaseModel):
    value1: str
    value2: str
    value3: str


def create_message(item: Item) -> str:

    names_map = {
        "HannibalMk": "jmarcosmn",
        "iFertz": "ifertz",
        "Renato Shimizu": "VictorShimizu",
        "cjosjr": "cjoseleijr",
    }
    if item.value2 in names_map:
        tele_name = names_map[item.value2]
    else:
        tele_name = item.value2

    return f"@{tele_name}, é o seu turno ({item.value3}) no game {item.value1}!"


def send_telegram_msg(msg: str) -> requests.Response:

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}
    data_dict = {
        "chat_id": CHAT_ID,
        "text": msg,
    }
    data = json.dumps(data_dict)
    return requests.post(url, data=data, headers=headers)


app = FastAPI()


@app.get("/")
def home_page():

    return "I'm Fred."


@app.post("/notify/")
def notify_telegram(item: Item):

    logging.debug(f"game_name: {item.value1} | player_name: {item.value2} | turn_number: {item.value3}")

    if item.value1 == "ignore":
        logging.debug("Request ignored.")
        return {"status": "ignored"}

    msg = create_message(item)
    resp = send_telegram_msg(msg)

    if resp.status_code != 200:
        logging.debug(f"Code: {resp.status_code} - Msg: {resp.json()['description']}.")
        return {"status": "nok"}

    logging.debug("Notification sent successfully.")
    return {"status": "ok"}
