# routes/index.py
from flask import Blueprint, render_template
from db import get_connection

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products ORDER BY id DESC")
            products = cursor.fetchall()
    finally:
        conn.close()
    return render_template('index.html', products=products)