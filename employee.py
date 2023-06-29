from flask import Blueprint, render_template, redirect, request, url_for, session
from db import user_dao

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route('/login')
def employee_login_form():
    """
    ログイン画面を表示する
    """
    return render_template('employee/login.html')

@employee_bp.route('login-exe', methods=['POST'])
def login_exe():
    """
    フォームの値を受取り、ログイン処理を実行する。
    ただし、パスワードが'0000'の場合は
    パスワード設定画面に遷移する 。
    """
    employee_id = request.form.get('employee_id')
    password = request.form.get('password')
    session['employee_id'] = employee_id

    if password == '0000':
        return redirect(url_for('employee.insert_login_info_form'))
    else:
        if user_dao.employee_login(employee_id, password):
            session['user'] = True
            return redirect(url_for('employee.employee_menu'))
        else:
            return redirect(url_for('employee_login_form'))


@employee_bp.route('/menu')
def employee_menu():
    """
    従業員メニュー画面に移行する。
    """
    return render_template('employee/menu.html')

@employee_bp.route('/edit-password-form')
def insert_login_info_form():
    """
    パスワード設定画面に遷移する
    """
    return render_template('employee/insert_login_info.html')

@employee_bp.route('/insert-login-info-exe', methods=['POST'])
def insert_login_info_exe():
    """
    パスワードの設定を実行する
    """
    employee_id = session['employee_id']
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    print(employee_id)
    print(password1)
    print(password2)

    error = False
    msg = ''
    if password1 != password2:
        error = True
        msg='パスワードに誤りがあります'

    if error:
        return redirect(url_for('employee.insert_login_info_form', msg=msg))

    count = user_dao.insert_login_info(employee_id, password1)
    if count:
        session.pop('employee_id', None)
        # ログイン処理
        return redirect(url_for('employee.employee_menu'))
    else:
        msg = '登録に失敗しました'
        return redirect(url_for('employee.insert_login_info_form', msg=msg))