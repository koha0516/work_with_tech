from flask import Blueprint, render_template, request, session, redirect, url_for
from db import user_dao
from function.gen_qrcode import gen_qr
from function.gen_employee_card import gen_employee_card
import random

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login')
def admin_login_form():
    """
    ログインフォーム画面を表示する
    """
    return render_template('admin/login.html')


@admin_bp.route('/login-exe', methods=['POST'])
def admin_login_exe():
    """
    ログイン処理を実行する
    """
    admin_id = request.form.get('admin_id')
    password = request.form.get('password')
    if user_dao.admin_login(admin_id, password):
        session['admin'] = True
        return redirect(url_for('admin.admin_menu'))
    else:
        msg='ログイン出来ませんでした'
        return redirect(url_for('admin.admin_login_form', msg=msg))

@admin_bp.route('/sign-up')
def admin_sign_up_form():
    """
    管理者登録画面を表示する
    """
    return render_template('admin/sign-up.html')

@admin_bp.route('/sign-up-exe', methods=['POST'])
def admin_sign_up_exe():
    """
    管理者登録処理を実行する
    """
    # セッションから値を受け取る
    admin_id = request.form.get('admin_id')
    employee_id = request.form.get('employee_id')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if password1 != password2:
        msg = 'パスワードに誤りがあります'
        return render_template('admin/sign-up.html', msg=msg)
    print(admin_id, employee_id, password1)
    if user_dao.register_admin(admin_id, employee_id, password1):
        session['admin'] = True
        return redirect(url_for('admin.admin_menu'))
    else:
        msg = '登録に失敗しました'
        return redirect(url_for('admin.admin_sign_up_form', msg=msg))


@admin_bp.route('/apply')
def admin_apply():
    """
    残業申請画面を表示する
    """
    return render_template('admin/apply.html')

@admin_bp.route('/menu')
def admin_menu():
    """
    管理者用メニュー画面を表示する
    """
    return render_template('admin/menu.html')

@admin_bp.route('/employee-list')
def admin_employee_list():
    """
    従業員一覧画面を表示する
    """
    d_id = request.args.get('department_id')
    if d_id:
        employees = user_dao.fetch_employees_by_department(d_id)
    else:
        employees = user_dao.fetch_all_employees()
    departments = user_dao.fetch_departments()
    return render_template('admin/employee-list.html', employees=employees, departments = departments)

@admin_bp.route('register_employee_form')
def register_employee_form():
    """
    従業員登録フォームを表示する
    """
    departments = user_dao.fetch_departments()
    roles = user_dao.fetch_roles()
    print(departments)
    print(roles)

    return render_template('admin/register-employee-form.html', departments = departments, roles = roles)

@admin_bp.route('/register_employee_confirm', methods=['POST'])
def register_employee_confirm():
    """
    従業員登録の確認画面を表示する。
    """
    name = request.form.get('name')
    mail = request.form.get('mail')
    department = request.form.get('department')
    role = request.form.get('role')

    employee = (name, mail, department, role)
    session['employee'] = employee

    return render_template('admin/register_employee_confirm.html', employee=employee)

@admin_bp.route('/register_employee_exe')
def register_employee_exe():
    """
    従業員登録処理を実行する
    """
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

        # 社員証を生成する
        gen_qr(employee_id)
        emp = (employee_id, name)
        gen_employee_card(emp, '/QR011112018.png')

        session['user'] = True
        return redirect(url_for('admin.register_employee_complete'))
    else:
        msg = '登録に失敗しました'
        return redirect(url_for('admin.register_employee_form'))

@admin_bp.route('register_employee_complete')
def register_employee_complete():
    """
    従業員登録完了画面を表示する
    """
    return render_template('admin/register-employee-complete.html')