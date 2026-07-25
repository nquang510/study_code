from flask import Blueprint, render_template, request, session, jsonify
from db import get_connection

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json(silent=True) or {}
    product_id = data.get('id')

    if not product_id:
        return jsonify({'success': False, 'message': 'Thiếu id sản phẩm'})

    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'id sản phẩm không hợp lệ'})

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
        return jsonify({'success': False, 'message': 'Sản phẩm không tồn tại'})

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
    session.modified = True 

    total_qty = sum(item['qty'] for item in cart)

    return jsonify({
        'success': True,
        'message': 'Đã thêm vào giỏ hàng',
        'cart_count': total_qty
    })


@cart_bp.route('/update-cart-qty', methods=['POST'])
def update_cart_qty():
    data = request.get_json(silent=True) or {}

    try:
        product_id = int(data.get('id'))
        new_qty = int(data.get('qty'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Dữ liệu không hợp lệ'})

    if new_qty <= 0:
        return jsonify({'success': False, 'message': 'Số lượng phải lớn hơn 0. Dùng nút xoá nếu muốn bỏ sản phẩm.'})

    cart = session.get('cart', [])

    target_item = None
    for item in cart:
        if item['id'] == product_id:
            item['qty'] = new_qty
            target_item = item
            break

    if not target_item:
        return jsonify({'success': False, 'message': 'Sản phẩm không có trong giỏ hàng'})

    session['cart'] = cart
    session.modified = True

    item_total = target_item['price'] * target_item['qty']
    cart_total = sum(i['price'] * i['qty'] for i in cart)
    cart_count = sum(i['qty'] for i in cart)

    return jsonify({
        'success': True,
        'qty': target_item['qty'],
        'item_total': item_total,
        'cart_total': cart_total,
        'cart_count': cart_count
    })


@cart_bp.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['qty'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


@cart_bp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json(silent=True) or {}

    try:
        product_id = int(data.get('id'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Dữ liệu không hợp lệ'})
    cart = session.get('cart', [])
    new_cart = [item for item in cart if item['id'] != product_id]


    session['cart'] = new_cart
    session.modified = True

    cart_total = sum(i['price'] * i['qty'] for i in new_cart)
    cart_count = sum(i['qty'] for i in new_cart)

    return jsonify({
        'success': True,
        'cart_total': cart_total,
        'cart_count': cart_count
    })