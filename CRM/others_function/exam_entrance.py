import psycopg2
from .hashed_password import check_password

from .replace import replacce


def exam_entrance(email, password):
    exist = False
    connection = psycopg2.connect(host='127.0.0.1',
                                  user='postgres',
                                  password='1111',
                                  database='postgres')
    cur = connection.cursor()
    cur.execute(f"SELECT email_or_number FROM reg")
    for email_db in cur.fetchall():
        if email == replacce(email_db):
            exist = True
            break

    if exist:
        cur.execute(f"SELECT hashed_password FROM data")
        for passw in cur.fetchall():
            if check_password(replacce(passw), password):
                return True
        connection.close()
    connection.close()
    return False
