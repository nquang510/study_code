import hashlib
from flask import Blueprint, render_template, request, session, redirect, url_for
from db import get_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    email = ""

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email:
            errors['email'] = 'Vui lòng nhập email'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'

        if not errors:
            hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE email=%s AND password=%s",
                        (email, hashed_password)
                    )
                    user = cursor.fetchone()
            finally:
                conn.close()

            if not user:
                errors['login'] = 'Email hoặc mật khẩu không đúng.'
            else:
                # Tạo session để đánh dấu đã đăng nhập + lưu id user
                session['is_login'] = True
                session['user_id'] = user['id']
                session['name'] = user['name']
                session['email'] = user['email']
                return redirect(url_for('index.index'))

    return render_template('login.html', errors=errors, email=email)