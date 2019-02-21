# -*- coding: utf-8 -*-

import vk_api
from utils_1 import get_random_id
import time
import requests
from bs4 import BeautifulSoup as bs
import json

vk = vk_api.VkApi(token="f78c56b538331269843e0aac3b7744a83194f5653a6e5241ad4e4724116e7f7b61b7ffcc2eddfdff93fc7")


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
            [get_button(label="Кто сегодня играет", color="positive")],
            [get_button(label="Новости футбола", color="primary")],
        ]
}

keyboard_start = {
    "one_time": False,
    "buttons":
        [
            [get_button(label="Начать", color="primary")]

        ]
}

keyboard_league = {
    "one_time": True,
    "buttons":
        [
            [
                get_button(label="Bundesliga", color="negative"),
                get_button(label="Premier League", color="primary"),

            ],
            [get_button(label="В главное меню", color="positive")],
        ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

keyboard_start = json.dumps(keyboard_start, ensure_ascii=False).encode('utf-8')
keyboard_start = str(keyboard_start.decode('utf-8'))

keyboard_league = json.dumps(keyboard_league, ensure_ascii=False).encode('utf-8')
keyboard_league = str(keyboard_league.decode('utf-8'))

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.65'
}

base_url = 'https://football24.ua/ru/calendar/'

session = requests.Session()
request = session.get(base_url, headers=headers)
if request.status_code == 200:
    soup = bs(request.content, "html.parser")
    tables = soup.find_all('table', attrs={'class': 'calendar-table'})

    for table in tables:
        title = table.find('tr', attrs={'class': 'calendar-game-info'}).text
        a = title.split()

        if a[-1] == 'прогноз':
            a = a[:-1]
        else:
            pass

        b = ' '.join(a)
else:
    print("ERROR")

while True:
    b = ' '.join(a)
    try:

        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if body.lower() == "начать":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Выбери кнопку на клавиатуре👇",
                                            "random_id": get_random_id(),
                                            "keyboard": keyboard})

            elif body.lower() == "кто сегодня играет":
                vk.method('messages.send', {'peer_id': id,
                                            "message": str(b),
                                            "random_id": get_random_id()})

            elif body.lower() == "новости футбола":
                vk.method("messages.send", {"peer_id": id, "message": "Выбери лигу",
                                            "random_id": get_random_id(),
                                            "keyboard": keyboard_league})

            elif body.lower() == "bundesliga":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "В конце первого тайма полузащитник гельзенкирхенцев Суат Сердар получил прямую красную карточку за грубейший фол на капитане «Фрайбурга» Майке Франце. Пострадавший не доиграл встречу и был заменен после первого тайма.",
                                            "attachment": "video-19835_456239406",
                                            "random_id": get_random_id(),
                                            "keyboard": keyboard_league})

            elif body.lower() == "premier league":
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Врач: Селихов и Мельгарехо вернутся в основу «Спартака» через день-два. \nВратарь Александр Селихов и полузащитник Лоренсо Мельгарехо вернутся в основную группу футболистов «Спартака» в ближайшие два дня, заявил руководитель медицинского департамента «красно-белых» Михаил Вартапетов.",
                                            "attachment": "photo-106522204_456245473",
                                            "random_id": get_random_id(),
                                            "keyboard": keyboard_league})

            elif body.lower() == "в главное меню":
                vk.method("messages.send",
                          {"peer_id": id, "message": "Выбери кнопку на клавиатуре👇", "random_id": get_random_id(),
                           "keyboard": keyboard})
        time.sleep(0.5)
    except Exception as E:
        time.sleep(1)
