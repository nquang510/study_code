import os
from flask import Blueprint, Flask, current_app, render_template, request, send_from_directory, session
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from routes.register import register_bp
from routes.login import login_bp
from routes.logout import logout_bp
from routes.account import account_bp
from routes.product import product_bp
from routes.index import index_bp

app = Flask(__name__)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(account_bp)
app.register_blueprint(product_bp)
app.register_blueprint(index_bp)
app.secret_key = '051005'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)

if __name__ == '__main__':
    app.run(debug=True)
    