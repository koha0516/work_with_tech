# テストデータ挿入のための単独実行ファイルです。
import psycopg2, os, random, csv

uri = os.environ['DATABASE_URL']
department = ['111', '112', '113', '121', '211', '212', '213', '221', '222']

with open('../static/csv/dummy.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    employees = [e for e in reader]

department_id_list = random.choices(department, k=100)

num_list = []
for de in department_id_list:
    # 役職コード　+ 所属コード　+ 社員番号
    num_list.append('01' + de + str(random.randrange(10000)).zfill(4))
# ランダムで社員番号を生成するメソッドを作る

count = 0

for emp in employees:
    tuple(emp)
    connection = psycopg2.connect(uri)
    cursor = connection.cursor()
    connection.set_client_encoding('utf-8')
    sql = f"""INSERT INTO employees (employee_id, name, mail, department_id, role, salt, password, flg, create_at)
    VALUES ({num_list[count]}, %s, %s, {department_id_list[count]}, '01', '0000', '0000', 1, CURRENT_TIMESTAMP(0))"""
    cursor.execute(sql, emp)
    connection.commit()
    cursor.close()
    connection.close()
    count = count + 1
