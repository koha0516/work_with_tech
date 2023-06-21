# from db import get_connection as gc
#
#
# def register_employee(employee):
#     sql = f"""INSERT INTO employees (employee_id, name, department_id, birth, gender, mail, tel, post_code, address, salt, password, join_at, create_at)
#                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP(0))"""
#     try:
#         connection = gc.get_connection()
#         cursor = connection.cursor()
#
#         cursor.execute(sql, employee)
#         count = cursor.rowcount
#         connection.commit()
#     except:
#         count = 0
#     finally:
#         cursor.close()
#         connection.close()
#
#     return count
#
