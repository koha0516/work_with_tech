from flask import Blueprint, render_template,redirect,url_for,request
from db import user_dao

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('login')
def admin_login():
    return render_template('admin/login.html')

@admin_bp.route('apply')
def admin_apply():
    return render_template('admin/apply.html')

@admin_bp.route('menu')
def admin_menu():
    return render_template('admin/menu.html')

@admin_bp.route('employee-list')
def admin_employee_list():
    return render_template('admin/employee-list.html')

@admin_bp.route('register_employee_form')
def register_employee_form():
    return render_template('admin/register-employee-form.html')

# @admin_bp.route('register_employee_exe', methods=['POST'])
# def register_employee_exe():
#     # 値を受け取る
#
#     user_name = request.form.get('username')
#     password = request.form.get('password')
#
#     # エラーチェック
#     if user_name == '':
#         error = 'ユーザ名が未入力です'
#         return render_template('register.html', error=error)
#     if password == '':
#         error = 'パスワードが未入力です'
#         return render_template('register.html', error=error, username=user_name)
#
#     # 実行
#     count = user_dao.register_employee(user_name)
#     if count == 1:
#         msg = '登録が完了しました'
#         return redirect(url_for('index', msg=msg))
#     else:
#         error = '登録に失敗しました'
#         return render_template('register.html', error=error)
