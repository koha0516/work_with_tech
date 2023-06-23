from flask import Blueprint, render_template, request, session, redirect, url_for
from db import user_dao
import random

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login')
def admin_login():
    return render_template('admin/login.html')

@admin_bp.route('/apply')
def admin_apply():
    return render_template('admin/apply.html')

@admin_bp.route('/menu')
def admin_menu():
    return render_template('admin/menu.html')

@admin_bp.route('/employee-list')
def admin_employee_list():
    return render_template('admin/employee-list.html')

@admin_bp.route('register_employee_form')
def register_employee_form():
    departments = user_dao.fetch_departments()
    roles = user_dao.fetch_roles()
    print(departments)
    print(roles)

    return render_template('admin/register-employee-form.html', departments = departments, roles = roles)

@admin_bp.route('/register_employee_confirm', methods=['POST'])
def register_employee_confirm():
    name = request.form.get('name')
    mail = request.form.get('mail')
    department = request.form.get('department')
    role = request.form.get('role')

    employee = (name, mail, department, role)
    session['employee'] = employee

    return render_template('admin/register_employee_confirm.html', employee=employee)

@admin_bp.route('/register_employee_exe')
def register_employee_exe():
    print(session['employee'])
    # セッションから値を受け取る
    name = session['employee'][0]
    mail = session['employee'][1]
    department = session['employee'][2]
    role = session['employee'][3]
    # 社員ID生成
    employee_id = role + department + str(random.randrange(10000)).zfill(4)
    # 登録処理
    employee = (employee_id, name, mail, department, role)
    print(employee)
    if user_dao.register_employee(employee):
        session.pop('employee', None)
        return redirect(url_for('admin.register_employee_complete'))
    else:
        msg = '登録に失敗しました'
        return redirect(url_for('admin.register_employee_form'))

@admin_bp.route('register_employee_complete')
def register_employee_complete():
    return render_template('admin/register-employee-complete.html')