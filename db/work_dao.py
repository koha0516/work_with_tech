import psycopg2
import os
from _datetime import datetime, time

def get_connection():
    """
    DB接続を行う
    """
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


# ---------- 打刻機能 --------------
def insert_bgn(employee_id, date):
    """
        出勤時刻を入力
    """
    now = datetime.now()
    now_time = now.strftime("%H:%M")
    print(now_time)

    sql = "INSERT INTO work_time (employee_id, working_date, begin) VALUES(%s, %s, %s) "

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (employee_id, date, now_time))
        count = cursor.rowcount
        connection.commit()
    except:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count

def insert_fin(employee_id, date):
    """
        退勤時刻を入力
    """
    now = datetime.now()
    now_time = now.strftime("%H:%M")
    print(now_time, employee_id, date)

    sql = "UPDATE work_time SET finish=%s WHERE employee_id=%s AND working_date=%s"

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (now_time, employee_id, date))
        count = cursor.rowcount
        connection.commit()
    except:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count

def insert_rest_bgn(employee_id, date):
    """
        休憩開始時刻を入力
    """
    now = datetime.now()
    now_time = now.strftime("%H:%M")
    print(now_time, employee_id, date)

    sql = "UPDATE work_time SET b_rest=%s WHERE employee_id=%s AND working_date=%s"

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (now_time, employee_id, date))
        count = cursor.rowcount
        connection.commit()
    except:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count

def insert_rest_fin(employee_id, date):
    """
        休憩終了時刻を入力
    """
    now = datetime.now()
    now_time = now.strftime("%H:%M")
    print(now_time, employee_id, date)

    sql = "UPDATE work_time SET f_rest=%s WHERE employee_id=%s AND working_date=%s"

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (now_time, employee_id, date))
        count = cursor.rowcount
        connection.commit()
    except:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count


# ---------- スケジュール（勤怠情報）取得 ------------
def fetch_employee_shifts(employee_id):
    """
    全ての勤怠情報を取得する
    :return:
    """
    sql = """
        SELECT working_date, begin, finish, b_rest, f_rest FROM work_time WHERE employee_id=%s
        """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (employee_id,))
        work_time = cursor.fetchall()
    except:
        return None
    finally:
        cursor.close()
        connection.close()

    return work_time


