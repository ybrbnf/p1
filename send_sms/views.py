from django.shortcuts import render
from service.models import Services
import requests
import json
import time
import configparser
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    service = Services.objects.order_by('-id')[:1]
    config = configparser.ConfigParser()
    config.read('settings.ini')
    account_elec = config.get('SMS', 'account_elec')
    account_gaz = config.get('SMS', 'account_gaz')
    phone_number_elec = config.get('SMS', 'phone_number_elec')
    phone_number_gaz = config.get('SMS', 'phone_number_gaz')
    elec = str(service[0].electricity)
    gaz = str(service[0].gaz)
    if len(elec) < 8:
        elec = '0'*(8-len(elec)) + elec
    if len(gaz) < 8:
        gaz = '0'*(8-len(gaz)) + gaz    
    context = {
        'title': 'Отправить показания счетчика электричества и газа',
        'message_elec' : '{} {}'.format(account_elec, elec),
        'message_gaz' : '{} {}'.format(account_gaz, gaz),
        'phone_number_elec' : phone_number_elec,
        'phone_number_gaz' : phone_number_gaz
                     }
    return render(request, 'send_sms/index.html', context)

@login_required

def end(request):  
    config = configparser.ConfigParser()
    config.read('settings.ini')
    answ = {}
    message = {}
    total_price=1
    phone_number_elec = request.POST.get('phone_number_elec', '')
    phone_number_gaz = request.POST.get('phone_number_gaz', '')
    message_elec = request.POST.get('message_elec', '')
    message_gaz = request.POST.get('message_gaz', '')
    login = config.get('SMS', 'login')       # Логин в smsc
    password = config.get('SMS', 'password')     # Пароль в smsc
    sender = ''    # Имя отправителя
    # Возможные ошибки
    errors = {
        1: 'Ошибка в параметрах.',
        2: 'Неверный логин или пароль.',
        3: 'Недостаточно средств на счете Клиента.',
        4: 'IP-адрес временно заблокирован из-за частых ошибок в запросах. Подробнее',
        5: 'Неверный формат даты.',
        6: 'Сообщение запрещено (по тексту или по имени отправителя).',
        7: 'Неверный формат номера телефона.',
        8: 'Сообщение на указанный номер не может быть доставлено.',
        9: 'Отправка более одного одинакового запроса на передачу SMS-сообщения либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты. '
    }
    # Отправка запроса
    url_gaz = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&sender=%s&fmt=3" % (login, password, phone_number_gaz, message_gaz, total_price, sender)
    answ['gaz'] = requests.get(url_gaz).json()
    url_elec = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&sender=%s&fmt=3" % (login, password, phone_number_elec, message_elec, total_price, sender)
    answ['elec'] = requests.get(url_elec).json()
    for item in answ:
        if 'error_code' in answ[item]:
        # Возникла ошибка
            message[item] = errors[answ[item]['error_code']]
        else:
            if total_price == 1:
        # Не отправлять, узнать только цену
                message[item] = 'Будут отправлены: {} SMS, цена рассылки: {}'.format(answ[item]['cnt'], answ[item]['cost'])
            else:
        # СМС отправлен, ответ сервера
                message[item] = answ[item]
    context = {
        'message': message,
        'title': 'Результат отправки смс',
               }
    return render(request, 'send_sms/send.html', context)

def send(request):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    api_id = config.get('SMS', 'api_id')
    message = {}
    phone_number_elec = request.POST.get('phone_number_elec', '')
    phone_number_gaz = request.POST.get('phone_number_gaz', '')
    message_elec = request.POST.get('message_elec', '')
    message_gaz = request.POST.get('message_gaz', '')
    url = 'https://sms.ru/sms/send?api_id=%s&to[%s]=%s&to[%s]=%s&json=1&test=1' % (api_id,
                                                                                   phone_number_elec,
                                                                                   message_elec,
                                                                                   phone_number_gaz,
                                                                                   message_gaz
                                                                                   )
    answ = requests.get(url).json()
    message = {}
    for item in answ['sms']:
        message[item] = config.get('Status_Codes', str(answ['sms'][item]['status_code']))
    context = {
               'message' : message,
               'title' : 'Результат отправки смс',
               }
    return render(request, 'send_sms/send.html', context)


