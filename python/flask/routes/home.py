from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__) # Định nghĩa Blueprint cho các route liên quan đến trang chủ

@home_bp.route('/')
def home():
    numbers = list(range(1, 11))
    return render_template('index.html')