import os
from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from db import get_connection

account_bp = Blueprint('account', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_login'):
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
                password = request.form.get('password', '').strip()
                avatar = request.files.get('avatar')

                if not name:
                    errors['name'] = 'Vui lòng nhập họ và tên'
                if not email:
                    errors['email'] = 'Vui lòng nhập email'

                if not errors:
                    cursor.execute(
                        "SELECT id FROM users WHERE email=%s AND id != %s",
                        (email, session['user_id'])
                    )
                    if cursor.fetchone():
                        errors['email'] = 'Email này đã được sử dụng bởi tài khoản khác'

                avatar_filename = None
                if avatar and avatar.filename != '':
                    if not allowed_file(avatar.filename):
                        errors['avatar'] = 'Chỉ cho phép file ảnh (png, jpg, jpeg, gif)'
                    else:
                        avatar.seek(0, os.SEEK_END)
                        size = avatar.tell()
                        avatar.seek(0)
                        if size > MAX_FILE_SIZE:
                            errors['avatar'] = 'Dung lượng ảnh phải nhỏ hơn 1MB'
                        else:
                            avatar_filename = avatar.filename

                if not errors:
                    import hashlib
                    if avatar_filename:
                        UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                        avatar.save(os.path.join(UPLOAD_FOLDER, avatar_filename))

                    if password:
                        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
                        if avatar_filename:
                            cursor.execute(
                                "UPDATE users SET name=%s, email=%s, password=%s, avatar=%s WHERE id=%s",
                                (name, email, hashed_password, avatar_filename, session['user_id'])
                            )
                        else:
                            cursor.execute(
                                "UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s",
                                (name, email, hashed_password, session['user_id'])
                            )
                    else:
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

                    session['name'] = name
                    session['email'] = email
                    success = 'Cập nhật thông tin thành công!'

            cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
            user = cursor.fetchone()
    finally:
        conn.close()

    return render_template('account.html', user=user, errors=errors, success=success)