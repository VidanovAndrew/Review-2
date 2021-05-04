import sqlite3
from sqlite3 import OperationalError
import Parser
from datetime import datetime


def update_main_news():
    print("make update")
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    # cur.execute("DROP TABLE MainNews")
    cur.execute('''CREATE TABLE IF NOT EXISTS MainNews
                  (date text, title text, content text, link real, most_common text, amount integer)''')

    News = Parser.ParseMainRBC()
    for i in range(len(News)):
        cur.execute("DELETE FROM MainNews where title= (?)", (News[i][1],))
    cur.executemany("insert or ignore into MainNews VALUES (?, ?, ?, ?, ?, ?)", News)
    cur.execute('SELECT * FROM MainNews')
    result = cur.fetchall()
    # print(result)
    con.commit()
    con.close()
    return result


def get_main_news(n):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM MainNews")
        results = cur.fetchmany(1)
    except OperationalError as e:
        update_main_news()
    cur.execute("SELECT * FROM MainNews")
    results = cur.fetchmany(int(n))
    if results[0][0] != str(datetime.now())[:10]:
        con.close()
        update_main_news()
        results = get_main_news(int(n))
    con.close()
    return results


def update_topic_news(topic):
    print("make topic update")
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    # cur.execute("DROP TABLE IF EXISTS {}".format(topic))
    cur.execute('''CREATE TABLE IF NOT EXISTS {}
                  (date text, title text, content text, link real, most_common text, amount integer)'''.format(topic))

    News = Parser.parse_topic(topic)
    for i in range(len(News)):
        cur.execute("DELETE FROM {} where title= (?)".format(topic), (News[i][1],))
    cur.executemany("insert or ignore into {} VALUES (?, ?, ?, ?, ?, ?)".format(topic), News)
    cur.execute('SELECT * FROM {}'.format(topic))
    result = cur.fetchall()
    # print(result)
    con.commit()
    con.close()
    return result


def get_topic_news(topic):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM {}".format(topic))
        results = cur.fetchmany(1)
    except OperationalError as e:
        update_topic_news(topic)
    cur.execute("SELECT * FROM {}".format(topic))
    results = cur.fetchmany(5)
    if results[0][0] != str(datetime.now())[:10]:
        con.close()
        update_topic_news(topic)
        results = get_topic_news(topic)
    con.close()
    return results


def describe_topic(topic):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM {}".format(topic))
        results = cur.fetchmany(1)
    except OperationalError as e:
        update_topic_news(topic)
    cur.execute("SELECT * FROM {}".format(topic))
    results = cur.fetchall()
    if results[0][0] != str(datetime.now())[:10]:
        con.close()
        update_topic_news(topic)
        results = get_topic_news(topic)
    con.close()
    return results


def get_article(name):
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    result = None
    try:
        cur.execute("SELECT * FROM MainNews WHERE title = (?)", (name, ))
        result = cur.fetchone()
    except BaseException as e:
        print(e)
    return result
