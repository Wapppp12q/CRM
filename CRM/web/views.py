import psycopg2
from django.shortcuts import render, redirect
import datetime
import shutil
import os
from validate_email import validate_email
import phonenumbers

from others_function.create_code import create_code
from others_function.sender import send_mail, send_sms
from others_function.create_secret_email import cr_sec_email
from others_function.hashed_password import set_password, check_password
from others_function.forms import RegistrationForm, VerificationForm, DataForm, Recovery, RDataForm, Entrance, PageForm
from others_function.replace import replacce
from others_function.exam_code import exam_code
from others_function.exam_password import exam_password
from others_function.exam_entrance import exam_entrance


PATH_DIC = r'C:\Users\artur\PycharmProjects\CRM_2\CRM\web\static\web\image'


def registration(request):
    code = create_code()
    error = ''
    valid = True
    number_exist = False
    email_exist = False

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if 'entrance' in request.POST:
            return redirect(f"/entrance")

        if form.is_valid():
            addr_or_number = form.cleaned_data.get('email_or_number')

            if validate_email(addr_or_number):
                email_exist = True
                #send_mail(addr_or_number, code, False)
            elif phonenumbers.parse(addr_or_number):
                number_exist = True
                #send_sms(addr_or_number, False, code)

            if number_exist or email_exist:
                connection = psycopg2.connect(user='postgres',
                                              password='1111',
                                              database='postgres',
                                              host='127.0.0.1')
                cursor = connection.cursor()
                cursor.execute(f"SELECT email_or_number FROM reg ")
                for item in cursor.fetchall():
                    if addr_or_number == replacce(*item):
                        valid = False
                        break
                if valid:
                    cursor.execute(f"INSERT INTO reg (email_or_number, code_ver) VALUES ('{addr_or_number}', {code})")
                    cursor.execute(f"SELECT id FROM reg WHERE email_or_number='{addr_or_number}'")
                    id_ver = int(replacce(cursor.fetchone()))
                    connection.commit()
                    connection.close()
                    if not number_exist:
                        addr_or_number = cr_sec_email(addr_or_number)
                    return redirect(f"/verification/{id_ver}/{addr_or_number}/False")

                else:
                    error = 'Такая почта уже зарегистрирована'
                connection.commit()
                connection.close()
            else:
                error = "Такой почты не существует"
        else:
            error = 'Введите данные'

    else:
        form = RegistrationForm()

    return render(request, 'web/registration.html', {'title': 'Регистрация', 'form': form, 'error': error, 'filename': 'registration'})


def verification(request, id_ver, sec_email, recovery):
    error = ''

    if request.method == 'POST':
        form = VerificationForm(request.POST)

        if form.is_valid():
            connection = psycopg2.connect(user='postgres',
                                          password='1111',
                                          database='postgres',
                                          host='127.0.0.1')
            cursor = connection.cursor()
            cursor.execute(f"SELECT code_ver FROM reg WHERE id={id_ver}")
            code_ver = replacce(cursor.fetchone())
            bool_code = exam_code(form.cleaned_data.get('code_ver'), code_ver)
            connection.close()

            if bool_code:
                if recovery == 'False':
                    return redirect(f'/registration_data/{id_ver}')
                else:
                    return redirect(f'/recovery_data/{int(id_ver)}/{sec_email}')
            else:
                error = 'Неверный код'

        else:
            error = 'Введите код'

    else:
        form = VerificationForm()

    return render(request, 'web/verification.html', {'title': 'Подтверждение почты', 'form': form, 'error': error,
                  'sec_email': sec_email, 'filename': 'verification'})


def registration_data(request, id_ver):
    error = ''
    connection = psycopg2.connect(user='postgres',
                                  password='1111',
                                  database='postgres',
                                  host='127.0.0.1')
    cursor = connection.cursor()
    cursor.execute('SELECT data_id FROM data')
    for id_db in cursor.fetchall():
        if id_ver == int(replacce(id_db)):
            return redirect('/error/Сраница не действительна')

    if request.method == 'POST':
        form = DataForm(request.POST)

        if 'registration' in request.POST:
            return redirect(f'/registration')

        if 'recovery' in request.POST:
            return redirect(f'/recovery')

        if form.is_valid():

            error = exam_password(request.POST.get('password1'), request.POST.get('password2'))
            if type(error) == bool:
                hashed_password = set_password(request.POST.get('password1'))
                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surname')
                created_data = datetime.datetime.now()
                cursor.execute(f"SELECT email_or_number FROM reg WHERE id={id_ver}")
                email = replacce(cursor.fetchone())
                cursor.execute(f"INSERT INTO data (name, surname, created_date, hashed_password, data_id) VALUES"
                               f" ('{name}', '{surname}', '{created_data}', '{hashed_password}', '{id_ver}')")
                connection.commit()
                avatar = f'/static/web/image/{email}/avatar.jpeg'
                cursor.execute(f"INSERT INTO page (avatar, page_id) VALUES"
                               f" ('{avatar}', {id_ver})")
                connection.commit()
                connection.close()
                direc = PATH_DIC + '/' + email
                os.mkdir(direc)
                shutil.copy('web/static/web/image/avatar.jpeg', f'web/static/web/image/{email}')
                return redirect(f'/page/{id_ver}')
        else:
            error = 'Введите данные'

    else:
        form = DataForm()

    return render(request, 'web/registration_data.html', {'title': 'Регистраци данных', 'form': form, 'error': error, 'filename': 'registration_data'})


def entrance(request):
    error = ''

    if request.method == 'POST':

        if 'registration' in request.POST:
            return redirect('/registration')

        if 'recovery' in request.POST:
            return redirect('/recovery')

        form = Entrance(request.POST)
        if form.is_valid():
            connection = psycopg2.connect(user='postgres',
                                          password='1111',
                                          database='postgres',
                                          host='127.0.0.1')
            cursor = connection.cursor()
            cursor.execute(f"SELECT id FROM reg WHERE email_or_number='{form.cleaned_data.get('email_or_number')}'")
            print(form.cleaned_data.get('email_or_number'))#udgfjJHGFhj12344$%^
            truth_user = exam_entrance(form.cleaned_data.get('email_or_number'), request.POST.get('password'))
            id = replacce(cursor.fetchone())

            if truth_user:
                return redirect(f'/page/{id}')
            else:
                error = 'Неверный логин или пароль'

        else:
            error = 'Введите данные'

    else:
        form = Entrance()

    return render(request, 'web/entrance.html', {'title': 'Вход', 'form': form, 'error': error, 'filename': 'entrance'})


def recovery(request):
    exam_email = False
    code = create_code()
    recovery = True
    error = ''

    if request.method == 'POST':
        form = Recovery(request.POST)

        if form.is_valid():
            connection = psycopg2.connect(user='postgres',
                                          password='1111',
                                          database='postgres',
                                          host='127.0.0.1')
            cursor = connection.cursor()
            cursor.execute("SELECT email_or_number FROM reg")
            for email_db in cursor.fetchall():
                email_db = replacce(*email_db)
                if str(form.cleaned_data.get('email_or_number')) == email_db:
                    exam_email = True
                    break
            if exam_email:
                sec_email = cr_sec_email(form.cleaned_data.get('email_or_number'))
                cursor.execute(f"SELECT id FROM reg WHERE email_or_number='{form.cleaned_data.get('email_or_number')}'")
                id_ver = int(replacce(cursor.fetchone()))
                #send_mail(form.cleaned_data('email_or_number'), code, recovery)
                cursor.execute(f"UPDATE reg SET code_ver={code} WHERE id={id_ver}")
                connection.commit()
                connection.close()
                return redirect(f'/verification/{id_ver}/{sec_email}/{recovery}')
            else:
                error = 'Аккаунта с такой почтой не существует'
        else:
            error = 'Введите данные'
    else:
        form = Recovery()
    return render(request, 'web/recovery.html', {'form': form, 'title': 'Восстановление пароля', 'error': error, 'filename': 'recovery'})


def recovery_data(request, id_ver, sec_email):
    error = ''
    id_ver = int(id_ver)

    if request.method == 'POST':
        form = RDataForm(request.POST)
        if form.is_valid():
            error = exam_password(request.POST.get('password1'), request.POST.get('password2'))
            if type(error) == bool:
                connection = psycopg2.connect(user='postgres',
                                              password='1111',
                                              database='postgres',
                                              host='127.0.0.1')
                cursor = connection.cursor()
                cursor.execute(f"UPDATE data SET hashed_password='{set_password(request.POST.get('password1'))}' WHERE data_id={id_ver}")
                connection.commit()
                connection.close()
                return redirect(f'/page/{id_ver}')
        else:
            error = 'Введите пароли'

    else:
        form = RDataForm()

    return render(request, 'web/recovery_data.html', {'form': form,
                  'title': 'Новый пароль', 'error': error, 'sec_email': sec_email, 'filename': 'recovery_data'})


def page(request, id_ver):
    connection = psycopg2.connect(user='postgres',
                                  password='1111',
                                  database='postgres',
                                  host='127.0.0.1')
    cur = connection.cursor()
    cur.execute(f"SELECT avatar FROM page WHERE page_id={id_ver}")
    source = replacce(str(cur.fetchone()))
    cur.execute(f"SELECT name FROM data WHERE data_id={id_ver}")
    name = replacce(str(cur.fetchone()))
    cur.execute(f"SELECT surname FROM data WHERE data_id={id_ver}")
    surname = replacce(str(cur.fetchone()))
    connection.close()

    if request.method == 'POST':
        form = PageForm(request.POST)
    else:
        form = PageForm()

    return render(request, 'web/page.html', {'title': 'Boot', 'form': form, 'source': source, 'name': name,
                                              'surname': surname, 'filename': 'page'})


def error(request, error_text):
    return render(request, 'web/error.html', {'error': error_text})
