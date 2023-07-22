import string, random, hashlib,psycopg2
import os

def get_connection():
    """
    DB接続を行う
    """
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection


# ---------- ユーザ登録・編集機能 --------------
def register_employee(employee):
    """
    DBに対して従業員の登録を行う
    """
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

def generate_salt():
    """
    ソルトを生成する
    """
    charset = string.ascii_letters + string.digits

    salt = ''.join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    """
    パスワードをハッシュ化する。
    """
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')

    hashed_pw = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1783).hex()
    return hashed_pw

def fetch_salt(employee_id):
    """
    従業員IDからソルトを取得する。
    初回ログインかどうかを判別するため(初回の場合'0000')
    :param employee_id:
    :return:
    """
    sql = 'SELECT salt FROM employees WHERE employee_id = %s'

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (employee_id,))
        user = cursor.fetchone()

        if user != None:
            print(user)
            salt = user[0]

    except psycopg2.DatabaseError:
        salt = 'error'
    finally:
        cursor.close()
        connection.close()

    return salt

def insert_login_info(employee_id, password):
    """
    新しいパスワードとソルトをDBに登録する
    :param employee_id:
    :param password:
    :return:
    """
    sql = "UPDATE employees SET salt=%s, password=%s WHERE employee_id=%s AND salt='0000' AND password='0000'"

    salt = generate_salt()
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

def register_admin(admin_id, employee_id, password):
    """
    DBに対して管理者の登録を行う
    :param employee:
    """
    sql = f"""INSERT INTO admin VALUES (%s, %s, %s, %s, 1, CURRENT_TIMESTAMP(0))"""

    salt = generate_salt()
    hashed_pw = get_hash(password, salt)

    try:
        connection = get_connection()
        cursor = connection.cursor()
#
        cursor.execute(sql, (admin_id, employee_id, salt, hashed_pw))
        count = cursor.rowcount
        connection.commit()
    except:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count


# ---------- ログイン機能 --------------
def employee_login(employee_id, password):
    """
    従業員ログインを行う
    :param employee_id:
    :param password:
    """
    sql = 'SELECT password, salt FROM employees WHERE employee_id = %s'
    flg = False

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (employee_id,))
        employee = cursor.fetchone()

        if employee != None:
            salt = employee[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == employee[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()

    return flg

def admin_login(admin_id, password):
    """
    管理者ログインを行う

    :param employee_id:
    :param password:
    """
    sql = 'SELECT password, salt FROM admin WHERE admin_id = %s'
    flg = False

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (admin_id,))
        admin = cursor.fetchone()

        if admin != None:
            salt = admin[1]

            hashed_password = get_hash(password, salt)

            if hashed_password == admin[0]:
                flg = True
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()

    return flg



# ---------- 従業員データ取得 --------------
def fetch_all_employees():
    """
    全ての従業員情報を取得する
    """
    sql = """
        SELECT employee_id, employees.name, departments.name, roles.name FROM employees 
        LEFT OUTER JOIN departments ON employees.department_id=departments.department_id
        LEFT OUTER JOIN roles ON employees.role=roles.role_id;
        """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql)
        employees = cursor.fetchall()
    except:
        return None
    finally:
        cursor.close()
        connection.close()

    return employees

def fetch_employees_by_department(department_id):
    """
    部署ごとの従業員情報を取得する
    :param department_id:
    :return:
    """
    sql = """
            SELECT employee_id, employees.name, departments.name, roles.name FROM employees 
            LEFT OUTER JOIN departments ON employees.department_id=departments.department_id
            LEFT OUTER JOIN roles ON employees.role=roles.role_id WHERE employees.department_id=%s;
            """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (department_id,))
        employees = cursor.fetchall()
    except:
        return None
    finally:
        cursor.close()
        connection.close()
    return employees


# ---------- 部署・役職データ取得 --------------
def fetch_departments():
    """
    全ての部署IDと部署名を取得する
    """
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

def fetch_roles():
    """
    全ての役職IDと役職名を取得する
    """
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
