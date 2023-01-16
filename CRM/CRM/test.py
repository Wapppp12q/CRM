from django.db import models
from django.db.models import QuerySet
from django import forms
from django.db import models
from django_pandas.managers import DataFrameManager

from django.db import models


class Consumer(models.Model):
    username = models.CharField(max_length=100, null=True)
    phone = models.BigIntegerField(null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.first_name


class Product(models.Model):
  product_name=models.TextField()
  objects = models.Manager()
  pdobjects = DataFrameManager()  # Pandas-Enabled Manager


class Authentication(models.Model):
    user_nickname = models.CharField('Никнейм', max_length=50)
    user_name = models.CharField('Имя оператора', max_length=50)
    user_lastname = models.CharField('Фамилие оператора', max_length=50)
    user_patronymic = models.CharField('Отчество оператора', max_length=50)

    user_birthday = models.DateField('Дата рождения')
    user_registration = models.DateField('Дата регистрации пользователя')

    user_phone = models.CharField('Телефон оператора', max_length=12)
    user_email = models.CharField('email', max_length=50)
    user_photo = models.CharField('потом будет фото', max_length=50)
    user_rang = models.IntegerField()

    def __str__(self):
        return self.user_nickname
    class Meta:
        verbose_name = 'Оператор'
        verbose_name_plural = 'Операторы'


class Task(models.Model):
    title = models.CharField('Название задачи', max_length=50)
    task = models.TextField('описание')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


