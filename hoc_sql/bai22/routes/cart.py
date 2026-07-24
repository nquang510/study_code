from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from db import get_connection

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json(silent=True) or {}
    product_id = data.get('id')

    if not product_id:
        return jsonify({'success': False, 'message': 'Thiếu id sản phẩm'}), 400

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'id sản phẩm không hợp lệ'}), 400

    # Lấy thông tin sản phẩm từ DB theo id
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, price, image FROM products WHERE id=%s",
                (product_id,)
            )
            product = cursor.fetchone()
    finally:
        conn.close()

    if not product:
        return jsonify({'success': False, 'message': 'Sản phẩm không tồn tại'}),

    cart = session.get('cart', [])

    found = False
    for item in cart:
        if item['id'] == product['id']:
            item['qty'] += 1
            found = True
            break

    if not found:
        cart.append({
            'id': product['id'],
            'title': product['title'],
            'price': float(product['price']),
            'image': product['image'],
            'qty': 1
        })

    session['cart'] = cart
    session.modified = True  # bắt buộc vì đang sửa list lồng trong session

    total_qty = sum(item['qty'] for item in cart)

    return jsonify({
        'success': True,
        'message': 'Đã thêm vào giỏ hàng',
        'cart_count': total_qty
    })


@cart_bp.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['qty'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


@cart_bp.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('cart.cart'))