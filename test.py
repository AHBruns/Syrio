import sqlite3

def t(s, c):
    try:
        c.execute(s)
    except sqlite3.OperationalError as ex:
        print(ex)