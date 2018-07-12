from bs4 import BeautifulSoup
import requests, re
from config import *


def site_name(url):
    """
    parse full url and returns the name of the site or default name
    """
    default_name = 'helpdesk.noc.dozortel.ru'
    site_split = url.split('/')
    for name in site_split:
        if name.endswith('.ru'):
            return name
    return default_name


def main_func(url):
    """
    tries to connect and log in. Returning the error or text keys
    """
    from requests.exceptions import ConnectionError, InvalidSchema
    s = requests.Session()
    url_auth = 'http://' + site_name(url) + '/' + URL_AUTH
    s.post(url_auth, data={'username': USERNAME, 'password': PASSWORD, 'refer_url': ''}, headers=HEADERS)
    try:
        r = s.get(url)
    except ConnectionError:
        return {'error': 'Ошибка соединения'}
    except InvalidSchema:
        return {'error': 'Проверьте URL на правильность'}
    if r.url == 'http://helpdesk.noc.dozortel.ru/cgi-bin/login.pl':
        return {'error': 'Не удалось авторизоваться, проверьте правильность учетной записи'}
    return {'text': r.text}


def parse_func(text, template=TEMPLATE, subject=True):
    """
    from the template it looks for all values
    """
    result = ''
    html_doc = text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('table', attrs={'id': 'work_order'})

    if not table:
        return 'Таблица ЗВР не найдена'
    if subject:
        result = 'ipres {}\n\n\n'.format(soup.find('span', attrs={'class', 'bigBold'}).string)
    for i in table.find_all('tr'):
        param = i.findAll('td')
        if len(param) < 2:
            continue

        join_params = ' '.join(param[0].strings)
        for t in template:
            if join_params and join_params.startswith(t.strip()):
                if len(param) == 3:
                    "Костыль осторожно"
                    sn = list(param[1].next_elements)[11]
                    result += '{}{}\n'.format(t, sn.string or '')
                if len(param) == 2:
                    result += '{}{}\n'.format(t, ' '.join(param[1].strings) or '')
    return result


def grep_all_email(text):
    """ find list email address"""
    return re.findall('[\w|\.]+@\w+\.\w+', text)


def grep_email(text):
    """ find email installer and manager and return dict"""
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
            get_email = '; '.join(grep_all_email(value_email))
            if not get_email:
                continue
            result[key_email] = get_email
    return result


def get_forms_internet(text):

    template_1 = [
        '№ заказа                                ',
        'Дата выпуска                            ',
        'Вид работ в точке подключения           ',
        'Перечень работ в точке подключения      ',
        'Вид работ на сети связи                 ',
        'Дополнительные сведения                 ',
    ]
    template_2 = [
        'Заказчик / оператор / агент             ',
        'Держатель договора (контракта)          ',
        'Адрес места установки                   ',
        'Точка терминации                        ',
        'Спутник ретранслятор (ТС)               ',
        'Модем                                   ',
        'РГН-код                                 ',
        'Наименование АЗССС (name)               ',
    ]
    template_3 = [
        'Договор (контракт, БЗ)                  ',
        'Оператор, предоставляющий услугу        ',
        'Конечный пользователь                   ',
        'Вид сервиса                             ',
        'Тип тарификации                         ',
        'Тариф (тарифный план)                   ',
        'Downstream CIR                          ',
        'Upstream CIR                            ',
    ]

    result = parse_func(text, template_1)
    if result == 'Таблица ЗВР не найдена':
        return 'Таблица ЗВР не найдена'
    result += '\nСтанция:\n'
    result += parse_func(text, template_2, subject=False)
    result += '\nУслуги:\n'
    result += parse_func(text, template_3, subject=False)
    return result


if __name__ == '__main__':

    '''url = 'http://' + site_name(URL) + '/' + URL
    get_zvr = main_func(url=url)
    
    parse_func(get_zvr)'''
    with open('zvr2.html', 'r') as f:
        file = f.read()
        print(get_forms_internet(file))

