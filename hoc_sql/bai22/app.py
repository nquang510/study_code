import os
from flask import Flask, send_from_directory, session
from routes.index import index_bp
from routes.register import register_bp
from routes.login import login_bp
from routes.logout import logout_bp
from routes.account import account_bp
from routes.product import product_bp
from routes.cart import cart_bp

app = Flask(__name__)
app.register_blueprint(index_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(account_bp)
app.register_blueprint(product_bp)
app.register_blueprint(cart_bp)
app.secret_key = '051005'


@app.context_processor
def inject_cart_count():
    # Tự động có sẵn biến cart_count ở MỌI template (header.html dùng để hiển thị badge)
    cart = session.get('cart', [])
    cart_count = sum(item['qty'] for item in cart)
    return dict(cart_count=cart_count)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)


if __name__ == '__main__':
    app.run(debug=True)