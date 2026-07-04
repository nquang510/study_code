from flask import Blueprint, current_app, render_template, request, session
import re # Thư viện regex để kiểm tra email
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
        files = request.files.getlist('avatar')
        if not email:
            errors['email'] = 'Vui lòng nhập email'
        elif not is_valid_email(email):
            errors['email'] = 'Vui lòng nhập đúng định dạng Email'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'
        if not errors:
            if 'email' not in session:
                errors['login'] = 'Không tìm thấy tài khoản. Vui lòng đăng ký trước.'
            else:
                saved_email = session.get('email')
                saved_password = session.get('password')
                if email == saved_email and password == saved_password:
                    return "Đăng nhập thành công!"
                else:
                    errors['login'] = 'Email hoặc mật khẩu không đúng.'            
    return render_template('login.html', errors=errors, email=email, password=password)

