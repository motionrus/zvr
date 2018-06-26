from bs4 import BeautifulSoup
import requests, re
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
    """
    from the template it looks for all values
    """
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
        join_params = ' '.join(param[0].strings)
        for t in TEMPLATE:
            if join_params and join_params.startswith(t.strip()):
                result += '{}{}\n'.format(t, param[1].string or '')
    return result


def grep_all_email(text):
    """ find list email address"""
    return re.findall('[\w|\.]+@\w+\.\w+', text)


def grep_email(text):
    """ find email installer and manager and return dict"""
    if text == 'Ошибка соединения':
        return text
    fields = EMAIL_TEMPLATE
    html_doc = text
    result = dict()
    soup = BeautifulSoup(html_doc, 'html.parser')
    email_finder = soup.findAll('td', text=fields)
    if email_finder:
        for email in email_finder:
            parent = email.find_parent()
            key_email = parent('td')[0].string
            value_email = parent('td')[1].string
            get_email = ', '.join(grep_all_email(value_email))
            result[key_email] = get_email
    return result


if __name__ == '__main__':
    '''get_zvr = main_func(url=URL)
    parse_func(get_zvr)'''
    with open('zvr.html', 'r') as f:
        file = f.read()
        grep_email(file)

