URL = 'http://helpdesk.noc.dozortel.ru/cgi-bin/request_view.pl?woMode=viewWO&woID=46812'
URL_AUTH = 'http://helpdesk.noc.dozortel.ru/cgi-bin/action.pl'
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
USERNAME = 'username'
PASSWORD = 'password'
TEMPLATE = [
    '№ заказа                                ',
    'Дата выпуска                            ',
    'Заказчик / оператор / агент             ',
    'Договор (контракт, БЗ)                  ',
    'Держатель договора (контракта)          ',
    'Оператор, предоставляющий услугу        ',
    'Конечный пользователь                   ',
    'Адрес места установки                   ',
    'Вид работ в точке подключения           ',
    'Вид работ на сети связи                 ',
    'Вид сервиса                             ',
    'Дополнительные параметры сервиса        ',
    'Тип тарификации                         ',
    'Тариф (тарифный план)                   ',
    'Модем                                   ',
    'Дополнительные сведения                 ',
    'РГН-код                                 ',
    'Наименование АЗССС (name)               ',
]
EMAIL_TEMPLATE = ['Контакты на месте установки', 'Контакты для оповещения', 'eMail']
