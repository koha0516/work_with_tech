import string, random, hashlib,psycopg2
import os

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection
# 従業員を登録する
def register_employee(employee):
    count=0
    sql = f"""INSERT INTO employees (employee_id, name, mail, department_id, role, salt, password, flg, create_at)
              VALUES (%s, %s, %s, %s, %s, '0000', '0000', 1, CURRENT_TIMESTAMP(0))"""
    try:
        connection = get_connection()
        cursor = connection.cursor()
#
        cursor.execute(sql, employee)
        count = cursor.rowcount
        connection.commit()
    except:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count


# 従業員のログイン情報を登録する
def get_salt():
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')

    hashed_pw = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1783).hex()
    return hashed_pw

def insert_login_info(employee_id, password):
    sql = "UPDATE employees SET salt=%s, password=$s WHERE employee_id=%s AND salt='0000' AND password='0000'"

    salt = get_salt()
    hashed_pw = get_hash(password, salt)

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (salt, hashed_pw, employee_id))

        count = cursor.rowcount  # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError:
        count = 0

    finally:
        cursor.close()
        connection.close()

    return count


# 部門一覧を取ってくる
def fetch_departments():
    sql = "SELECT * FROM departments"
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql)
        departments = cursor.fetchall()
    except:
        return None
    finally:
        cursor.close()
        connection.close()

    return departments

# 役職一覧を取ってくる
def fetch_roles():
    sql = "SELECT * FROM roles"
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql)
        roles = cursor.fetchall()
    except:
        return None
    finally:
        cursor.close()
        connection.close()

    return roles
