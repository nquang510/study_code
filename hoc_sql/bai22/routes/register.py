import os
import hashlib
from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from db import get_connection

register_bp = Blueprint('register', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    email = ""
    name = ""
    show_success = session.pop('register_success', False)

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('name', '').strip()
        avatar = request.files.get('avatar')

        # ---- Validate từng input ----
        if not email:
            errors['email'] = 'Vui lòng nhập email'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'
        if not name:
            errors['name'] = 'Vui lòng nhập họ tên'

        if not avatar or avatar.filename == '':
            errors['avatar'] = 'Vui lòng chọn ảnh đại diện'
        else:
            if not allowed_file(avatar.filename):
                errors['avatar'] = 'Chỉ cho phép file ảnh (png, jpg, jpeg, gif)'
            else:
                avatar.seek(0, os.SEEK_END)
                size = avatar.tell()
                avatar.seek(0)  # trả con trỏ về đầu để lưu file sau này
                if size > MAX_FILE_SIZE:
                    errors['avatar'] = 'Dung lượng ảnh phải nhỏ hơn 1MB'

        # ---- Kiểm tra email đã tồn tại chưa ----
        if not errors:
            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
                    if cursor.fetchone():
                        errors['email'] = 'Email này đã được đăng ký'
            finally:
                conn.close()

        # ---- Nếu hợp lệ: lưu file + insert DB ----
        if not errors:
            UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = avatar.filename
            avatar.save(os.path.join(UPLOAD_FOLDER, filename))

            # Mã hoá mật khẩu bằng MD5
            hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (email, password, name, avatar) VALUES (%s, %s, %s, %s)",
                        (email, hashed_password, name, filename)
                    )
                conn.commit()
            finally:
                conn.close()

            session['register_success'] = True
            return redirect(url_for('register.register'))

    return render_template('register.html', errors=errors, email=email, name=name, success=show_success)