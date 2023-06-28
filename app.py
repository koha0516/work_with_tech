from flask import Flask, render_template, session, redirect
import random, string
from employee import employee_bp
from admin import admin_bp

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

app.register_blueprint(employee_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def top_menu():  # put application's code here
    return render_template('top-menu.html')

def logout():
    # ログアウト処理
    return redirect('top_menu')

if __name__ == '__main__':
    app.run(debug=True)
