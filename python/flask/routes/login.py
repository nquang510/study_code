import os
from flask import Blueprint, current_app, render_template, request
import re # Thư viện regex để kiểm tra email
from werkzeug.security import generate_password_hash, check_password_hash # Thư viện để mã hóa mật khẩu

login_bp = Blueprint('login', __name__)
# Tạo một tập hợp bao gồm đuôi file được phép tải lên và giới hạn kích thước file
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE_MB = 1

# Hàm để lấy tên file sử dụng hàm rsplit() để tách dấu . ra và lấy đuôi file, chuyển sang chữ thường và kiểm tra xem có trong mảng không
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file_upload(files):
    result = {
        "success": False,
        "error": None,
    }
    
    for file in files:
        if not file or file.filename == '':
            result["error"] = "Vui lòng chọn file"
            return result
        if not allowed_file(file.filename):
            result["error"] = "Chỉ cho phép tải lên các file ảnh (png, jpg, jpeg, gif)"
            return result
        file.seek(0, os.SEEK_END)  # Di chuyển con trỏ đến cuối file để lấy kích thước
        file_size = file.tell()
        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
            result["error"] = "File quá lớn"
            return result
        result["success"] = True
    return result

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.-]+$'
    return re.match(pattern, email) is not None

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    email = ""
    password = ""
    files = []
    
    if request.method == 'POST':
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()
        files = request.files.getlist('avatar')
        if not email:
            errors['email'] = 'Vui lòng nhập email'
        elif not is_valid_email(email):
            errors['email'] = 'Email không hợp lệ'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'
        if len(files) > 3:
            errors['file'] = "Chỉ được tải lên tối đa 3 file"
        else:
            upload_result = handle_file_upload(files)
            if not upload_result["success"]:
                errors['file'] = upload_result["error"]
        if not errors:
            hashed_password = generate_password_hash(password) # Mã hóa mật khẩu
            UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
            # Tạo thư mục uploads nếu chưa có
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            for file in files:
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
            return "Đăng nhập thành công!"
            
    return render_template('login.html', errors=errors, email=email, password=password)

