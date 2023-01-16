from django.db.models import DateField, Model, IntegerField, EmailField, ForeignKey, CharField, CASCADE

import psycopg2

connection = psycopg2.connect(
        host='127.0.0.1',
        user='postgres',
        password='1111',
        database='postgres'
    )

try:
    with connection.cursor() as cursor:
        cursor.execute(
          """CREATE TABLE reg(
             id SERIAL PRIMARY KEY ,
             email_or_number varchar(50) NOT NULL,
             code_ver INTEGER NOT NULL)"""
        )

        cursor.execute(
          """CREATE TABLE data(
             id SERIAL PRIMARY KEY,
             name varchar(300) NOT NULL,
             surname varchar(300) NOT NULL,
             hashed_password varchar(300) NOT NUlL,
             created_date varchar(300),
             Data_Id INTEGER,
             FOREIGN KEY (Data_Id) REFERENCES reg(id))"""
        )

        cursor.execute(
          """CREATE TABLE page(
             id  SERIAL PRIMARY KEY,
             avatar varchar(1000),
             Page_Id INTEGER,
             FOREIGN KEY (Page_Id) REFERENCES reg (id))"""
              )

except psycopg2.errors.DuplicateTable:
    pass

finally:
    connection.commit()
    connection.close()


# class Registration(Model):
#     id = IntegerField(primary_key=True)
#     email_or_number = CharField(max_length=200)
#     code_ver = IntegerField()
#
#     def __repr__(self):
#         return self.id
#
#
# class Data(Model):
#     id = IntegerField(primary_key=True)
#     name = CharField(max_length=10000)
#     surname = CharField(max_length=10000)
#     hashed_password = CharField(max_length=10000)
#     created_date = DateField()
#     user = ForeignKey(Registration, on_delete=CASCADE)
#
#     def __repr__(self):
#         return self.id
#
#
# class Page(Model):
#     id = IntegerField(primary_key=True)
#     avatar = CharField(max_length=10000)
#     page = ForeignKey(Registration, on_delete=CASCADE)
#
#     def __repr__(self):
#         return self.id

