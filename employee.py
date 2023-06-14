from flask import Blueprint, render_template

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.route('login')
def employee_login():
    return render_template('employee/login.html')

@employee_bp.route('menu')
def employee_menu():
    return render_template('employee/menu.html')