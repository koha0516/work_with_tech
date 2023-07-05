import psycopg2
import os

def get_connection():
    """
    DB接続を行う
    """
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


def insert_bgn(employee_id, date):
    sql = "INSERT INTO work_time (employee_id, working_date, begin) VALUES(%s, %s, CURRENT_TIME) "

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (employee_id, date))
        count = cursor.rowcount
        connection.commit()
    except:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count

def insert_fin(employee_id, date):
    sql = "UPDATE work_time SET finish=%s WHERE employee_id=%s date=%s"


def insert_bgn_rest(employee_id, date):
    pass


def insert_fin_rest(employee_id, date):
    pass


def insert_holiday(employee_id, date):
    pass


def insert_overtime(employee_id, date):
    pass


