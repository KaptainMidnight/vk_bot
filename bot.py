import json
import vk_api
from utils_1 import get_random_id
import time
import parsing

vk = vk_api.VkApi(token="c34bd08d3ef28010f9e794630f0d4fd24d73f126139cd020c7c965f216b5528153c64a3558be0a6f58ca2")


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


keyboard = {
    "one_time": False,
    "buttons":
    [
        [get_button(label="Кто сегодня играет🏆⚽️", color="positive")],
    ]
}

keyboard_start = {
    "one_time": False,
    "buttons":
    [
        [get_button(label="Начать", color="primary")]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard_start = json.dumps(keyboard_start, ensure_ascii=False).encode('utf-8')
keyboard_start = str(keyboard_start.decode('utf-8'))

while True:
    try:

        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if body.lower() == "начать":
                vk.method("messages.send", {"peer_id": id, "message": "Выбери кнопку на клавиатуре👇", "random_id": get_random_id(), "keyboard": keyboard})
            elif body.lower() == "кто сегодня играет🏆⚽":
               vk.method("messages.send", {"peer_id": id, "message": parsing.parsing_site(), "random_id": get_random_id()})

        time.sleep(0.5)
    except Exception as E:
        time.sleep(1)
