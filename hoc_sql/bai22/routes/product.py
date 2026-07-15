import os
from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from db import get_connection

product_bp = Blueprint('product', __name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login.login'))
        return func(*args, **kwargs)
    return wrapper

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------- DANH SÁCH PRODUCT CỦA MEMBER -------------------
@product_bp.route('/my-product')
@login_required
def my_product():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM products WHERE id_user=%s ORDER BY id DESC",
                (session['user_id'],)
            )
            products = cursor.fetchall()
    finally:
        conn.close()

    return render_template('my_product.html', products=products)


# ------------------- ADD PRODUCT -------------------
@product_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    errors = {}
    title = ""
    price = ""

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        price = request.form.get('price', '').strip()
        image = request.files.get('image')

        if not title:
            errors['title'] = 'Vui lòng nhập tên sản phẩm'
        if not price:
            errors['price'] = 'Vui lòng nhập giá'
        else:
            try:
                price_value = float(price)
                if price_value < 0:
                    errors['price'] = 'Giá không hợp lệ'
            except ValueError:
                errors['price'] = 'Giá phải là số'
        if not image or image.filename == '':
            errors['image'] = 'Vui lòng chọn ảnh sản phẩm'
        elif not allowed_file(image.filename):
            errors['image'] = 'Chỉ cho phép ảnh png, jpg, jpeg, gif'

        if not errors:
            UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))

            conn = get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO products (title, price, image, id_user) VALUES (%s, %s, %s, %s)",
                        (title, price_value, filename, session['user_id'])
                    )
                conn.commit()
            finally:
                conn.close()

            return redirect(url_for('product.my_product'))

    return render_template('add_product.html', errors=errors, title=title, price=price)


# ------------------- EDIT PRODUCT -------------------
@product_bp.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Chỉ cho sửa product của chính mình
            cursor.execute(
                "SELECT * FROM products WHERE id=%s AND id_user=%s",
                (product_id, session['user_id'])
            )
            product = cursor.fetchone()

        if not product:
            return redirect(url_for('product.my_product'))

        errors = {}
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            price = request.form.get('price', '').strip()
            image = request.files.get('image')

            if not title:
                errors['title'] = 'Vui lòng nhập tên sản phẩm'
            if not price:
                errors['price'] = 'Vui lòng nhập giá'
            else:
                try:
                    price_value = float(price)
                    if price_value < 0:
                        errors['price'] = 'Giá không hợp lệ'
                except ValueError:
                    errors['price'] = 'Giá phải là số'

            if image and image.filename != '' and not allowed_file(image.filename):
                errors['image'] = 'Chỉ cho phép ảnh png, jpg, jpeg, gif'

            if not errors:
                filename = product['image']  # giữ ảnh cũ nếu không upload ảnh mới
                if image and image.filename != '':
                    UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(UPLOAD_FOLDER, filename))

                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE products SET title=%s, price=%s, image=%s WHERE id=%s AND id_user=%s",
                        (title, price_value, filename, product_id, session['user_id'])
                    )
                conn.commit()
                return redirect(url_for('product.my_product'))

            # Nếu có lỗi, cập nhật lại product tạm để hiển thị đúng giá trị vừa nhập
            product['title'] = title
            product['price'] = price
    finally:
        conn.close()

    return render_template('edit_product.html', errors=errors, product=product)


# ------------------- DELETE PRODUCT -------------------
@product_bp.route('/delete-product/<int:product_id>')
@login_required
def delete_product(product_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Chỉ cho xoá product của chính mình
            cursor.execute(
                "DELETE FROM products WHERE id=%s AND id_user=%s",
                (product_id, session['user_id'])
            )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('product.my_product'))