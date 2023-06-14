from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('login')
def admin_login():
    return render_template('admin/login.html')

@admin_bp.route('apply')
def admin_apply():
    return render_template('admin/apply.html')