from django.forms import EmailField, Form, CharField, PasswordInput


class RegistrationForm(Form):
    email_or_number = CharField(label='Введите вашу почту или номер телефона')


class VerificationForm(Form):
    code_ver = CharField(label='Письмо отправлено')


class DataForm(Form):
    name = CharField(label='Имя:')
    surname = CharField(label='Фамилия:')


class Recovery(Form):
    email_or_number = CharField(label='Введите почту или номер телефона, на который зарегистрирован аккаунт:')


class RDataForm(Form):
    password = PasswordInput()
    pass_exam = PasswordInput()


class Entrance(Form):
    email_or_number = CharField(label='Почта:')
    password = PasswordInput(render_value=True)


class PageForm(Form):
    status = CharField()