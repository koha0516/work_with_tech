from flask import Blueprint, render_template

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

@admin_bp.route('employees')
def admin_employee_list():
    return render_template('admin/employee-list.html')