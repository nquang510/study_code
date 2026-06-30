from flask import Blueprint, render_template, request
import re # Thư viện regex để kiểm tra email
from werkzeug.security import generate_password_hash, check_password_hash # Thư viện để mã hóa mật khẩu

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
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()
        if not email:
            errors['email'] = 'Vui lòng nhập email'
        elif not is_valid_email(email):
            errors['email'] = 'Email không hợp lệ'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'
        if not errors:
            hashed_password = generate_password_hash(password) # Mã hóa mật khẩu
            return f"Đăng nhập thành công! Mật khẩu đã được mã hóa: {hashed_password}"
    return render_template('login.html', errors=errors, email=email, password=password)

