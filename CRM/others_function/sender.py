import smtplib
from email.mime.text import MIMEText
import urllib
import json


def send_mail(email, code, rec):
    addr_from = "veryficationproj@gmail.com"
    password = '3pz6~ZT1LEW|RSW'

    body = f"Здравствуйте! Код подтверждения регистрации {email} - {code}."
    if rec:
        body = f"Здравствуйте! Код восстановления пароля {email} - {code}."
    msg = MIMEText(body)
    msg['Subject'] = 'Код активации'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(addr_from, password)
    server.sendmail(addr_from, email, msg.as_string())


def send_sms(phone, rec, code, total_price=0):
    text = f"Здравствуйте! Код подтверждения регистрации {phone} - {code}."
    if rec:
        text = f"Здравствуйте! Код восстановления пароля {phone} - {code}."

    login = 'userlog'
    password = 'myPas1'
    sender = 'Python'
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

    url = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&sender=%s&fmt=3" % (
    login, password, phone, text, total_price, sender)
    answer = json.loads(urllib.urlopen(url).read())
    if 'error_code' in answer:
        # Возникла ошибка
        return errors[answer['error_code']]
    else:
        if total_price == 1:
            # Не отправлять, узнать только цену
            print
            'Будут отправлены: %d SMS, цена рассылки: %s' % (answer['cnt'], answer['cost'].encode('utf-8'))
        else:
            # СМС отправлен, ответ сервера
            return answer