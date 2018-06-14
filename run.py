from bs4 import BeautifulSoup
import requests
from config import *


def main_func(url):
    from requests.exceptions import ConnectionError
    s = requests.Session()
    s.post(URL_AUTH, data={'username': USERNAME, 'password': PASSWORD, 'refer_url': ''}, headers=HEADERS)
    try:
        r = s.get(url)
    except ConnectionError:
        return 'Ошибка соединения'
    if r.url == 'http://helpdesk.noc.dozortel.ru/cgi-bin/login.pl':
        return {'error': 'Не удалось авторизоваться, проверьте правильность учетной записи'}
    return r.text


def parse_func(text):
    if text == 'Ошибка соединения':
        return text
    result = ''
    html_doc = text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('table', attrs={'id': 'work_order'})

    if not table:
        return 'таблица ЗВР не найдена'
    result = 'ipres {}\n\n\n'.format(soup.find('span', attrs={'class', 'bigBold'}).string)
    for i in table.find_all('tr'):
        param = i.findAll('td')
        for t in TEMPLATE:
            if param[0].string == t.strip():
                result += '{}{}\n'.format(t, param[1].string or '')

    return result


if __name__ == '__main__':
    get_zvr = main_func(url=URL)
    parse_func(get_zvr)
