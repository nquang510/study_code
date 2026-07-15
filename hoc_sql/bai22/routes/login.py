from flask import Blueprint, render_template, request, session, redirect, url_for
import re
from werkzeug.security import check_password_hash
from db import get_connection

login_bp = Blueprint('login', __name__)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+$'
    return re.match(pattern, email) is not None

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    email = ""
    password = ""

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email:
            errors['email'] = 'Vui lòng nhập email'
        elif not is_valid_email(email):
            errors['email'] = 'Vui lòng nhập đúng định dạng Email'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'

        if not errors:
            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                    user = cursor.fetchone()
            finally:
                conn.close()

            if not user:
                errors['login'] = 'Không tìm thấy tài khoản. Vui lòng đăng ký trước.'
            elif not check_password_hash(user['password'], password):
                errors['login'] = 'Email hoặc mật khẩu không đúng.'
            else:
                # Đăng nhập thành công -> lưu thông tin vào session
                session['user_id'] = user['id']
                session['email'] = user['email']
                session['name'] = user['name']
                return redirect(url_for('home.home'))

    return render_template('login.html', errors=errors, email=email, password=password)