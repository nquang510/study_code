import os
from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from db import get_connection

account_bp = Blueprint('account', __name__)

# Decorator chặn truy cập nếu chưa đăng nhập
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login.login'))
        return func(*args, **kwargs)
    return wrapper

@account_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    errors = {}
    success = None
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                name = request.form.get('name', '').strip()
                email = request.form.get('email', '').strip()
                avatar_file = request.files.get('avatar')

                if not name:
                    errors['name'] = 'Vui lòng nhập họ và tên'
                if not email:
                    errors['email'] = 'Vui lòng nhập email'

                # Kiểm tra email trùng với TÀI KHOẢN KHÁC (khác id của mình)
                if not errors:
                    cursor.execute(
                        "SELECT id FROM users WHERE email=%s AND id != %s",
                        (email, session['user_id'])
                    )
                    if cursor.fetchone():
                        errors['email'] = 'Email này đã được sử dụng bởi tài khoản khác'

                if not errors:
                    avatar_filename = None
                    if avatar_file and avatar_file.filename != '':
                        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                        avatar_filename = secure_filename(avatar_file.filename)
                        avatar_file.save(os.path.join(UPLOAD_FOLDER, avatar_filename))

                    if avatar_filename:
                        cursor.execute(
                            "UPDATE users SET name=%s, email=%s, avatar=%s WHERE id=%s",
                            (name, email, avatar_filename, session['user_id'])
                        )
                    else:
                        cursor.execute(
                            "UPDATE users SET name=%s, email=%s WHERE id=%s",
                            (name, email, session['user_id'])
                        )
                    conn.commit()

                    # Cập nhật lại session để header hiển thị đúng tên/email mới
                    session['name'] = name
                    session['email'] = email
                    success = 'Cập nhật thông tin thành công!'

            # Luôn lấy thông tin mới nhất để hiển thị lên form
            cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
            user = cursor.fetchone()
    finally:
        conn.close()

    return render_template('account.html', user=user, errors=errors, success=success)

