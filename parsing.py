import requests
from bs4 import BeautifulSoup as bs


def parsing_site():

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
            a = a[:-1]
            b = ' '.join(a)
    else:
        print("ERROR")
