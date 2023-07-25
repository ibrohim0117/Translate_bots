import os
import psycopg2
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

con = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')

)
cur = con.cursor()


def creat_table():
    kod = '''
    CREATE TABLE IF NOT EXISTS uzb_english(
        id serial primary key,
        user_id varchar(100) not null,
        user_name varchar(100),
        time_reg timestamp default now()
    );'''

    cur = con.cursor()  # noqa
    cur.execute(kod)
    con.commit()
    # cur.close()


def reg(user_id: int, user_name: str):
    qur = 'insert into uzb_english(user_id, user_name) values (%s,%s)'
    cur.execute(qur, (user_id, user_name))
    con.commit()


def chek():
    l = []
    qur = 'select user_id from uzb_english;'
    cur.execute(qur, )
    for i in cur.fetchall():
        l.append(*i)
    return l


kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
b = KeyboardButton(text="📋 E'lon joylash")
kb.add(b)


class Habar(StatesGroup):
    letter = State()