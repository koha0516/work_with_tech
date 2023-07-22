import calendar

from flask import Blueprint, render_template, redirect, request, url_for, session
from db import user_dao, work_dao
from function.read_qrcode import read_qrcode
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from function import date_util_fn

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


# ---------- ログイン・ログイン情報編集機能 --------------
@employee_bp.route('/login')
def login_form():
    """
    ログイン画面を表示する
    """
    return render_template('employee/login.html')

@employee_bp.route('login-exe', methods=['POST'])
def login_exe():
    """
    フォームの値を受取り、ログイン処理を実行する。
    ただし、入力されたパスワードが'0000'の場合は
    パスワード設定画面に遷移する 。
    """
    employee_id = request.form.get('employee_id')
    password = request.form.get('password')
    session['employee_id'] = employee_id

    if password == '0000' and user_dao.fetch_salt(employee_id) == '0000':
        return redirect(url_for('employee.insert_login_info_form'))
    else:
        if user_dao.employee_login(employee_id, password):
            session['user'] = True
            session['employee_id'] = employee_id
            return redirect(url_for('employee.employee_menu'))
        else:
            return redirect(url_for('employee.login_form'))

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


# -------------- 従業員メニュー表示 --------------------
@employee_bp.route('/menu')
def employee_menu():
    """
    従業員メニュー画面に移行する。
    """
    return render_template('employee/menu.html')


# ------------------ 勤怠管理 打刻機能 ----------------------
@employee_bp.route('/begin')
def punch_a_beginning_time():
    """
    出勤時刻を記録する
    """
    employee_id = read_qrcode()
    today = datetime.today().date()

    if work_dao.insert_bgn(employee_id, today):
        return redirect(url_for('top_menu', msg='出勤時刻を記録しました'))
    else:
        return redirect(url_for('top_menu', msg='打刻できませんでした'))

@employee_bp.route('/finish')
def punch_a_finish_time():
    """
    退勤時刻を記録する
    """
    employee_id = read_qrcode()
    today = datetime.today().date()

    if work_dao.insert_fin(employee_id, today):
        return redirect(url_for('top_menu', msg='退勤時刻を記録しました'))
    else:
        return redirect(url_for('top_menu', msg='打刻できませんでした'))

@employee_bp.route('/begin-rest')
def bgn_rest():
    """
    休憩開始時刻を記録する
    """
    employee_id = read_qrcode()
    today = datetime.today().date()

    if work_dao.insert_rest_bgn(employee_id, today):
        return redirect(url_for('top_menu', msg='休憩開始'))
    else:
        return redirect(url_for('top_menu', msg='打刻できませんでした'))

@employee_bp.route('/finish-rest')
def fin_rest():
    """
    休憩終了時刻を記録する
    """
    employee_id = read_qrcode()
    today = datetime.today().date()

    if work_dao.insert_rest_fin(employee_id, today):
        return redirect(url_for('top_menu', msg='休憩終了'))
    else:
        return redirect(url_for('top_menu', msg='打刻できませんでした'))


# ------------------ 残業に関する機能 ----------------------
@employee_bp.route('/overtime-apply')
def overtime_apply():
    """
    残業申請画面を表示する
    """
    return render_template('employee/employee-apply.html')


# ------------------ スケジュール確認機能 ----------------------
@employee_bp.route('/schedule')
def schedule():
    """
    スケジュールを表示する
    """
    today = date.today()
    f = today.strftime('%Y-%m') + '-01'
    first = date.fromisoformat(f)

    w, d = calendar.monthrange(today.year, today.month)
    days = []
    employee_id = session['employee_id']
    shifts = work_dao.fetch_employee_shifts(employee_id)
    shifts.append("a")
    print(shifts)

    index=0
    for i in range(d):
        week_day = first.weekday()
        str_week_day = date_util_fn.day_of_week(week_day)
        str_date = first.strftime('%Y-%m-%d')
        if first == shifts[index][0]:

            rest =  datetime.combine(date.today(), shifts[index][4]) - datetime.combine(date.today(), shifts[index][3])
            days.append([str_week_day, str_date, shifts[index][1], shifts[index][2], rest])
            index += 1
        else:
            days.append([str_week_day, str_date,"","",""])
        first = first + relativedelta(days=1)

    print(days)
    # 曜日を表す数値と、一か月分の日付を表すstr型リストを送る
    return render_template('employee/schedule.html', days = days) #work_days=work_days
