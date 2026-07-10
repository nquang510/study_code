from flask import Flask, render_template, request, redirect
from db import get_connection

app = Flask(__name__)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        #Lấy dữ liệu từ form
        name = request.form['name']
        price = request.form['price']
        
        #Kết nối mysql
        conn = get_connection()
        cur = conn.cursor()

        #Insert dữ liệu
        cur.execute(
            "INSERT INTO product (name, price) VALUES (%s, %s)", (name, price)
        )
        
        #Lưu dữ liệu xuống db
        conn.commit()
        
        #Đóng kết nối
        cur.close()
        conn.close()
        
        #Sau khi xong quay lại trang add_product
        return redirect('/add_product')
    #Nếu người dùng truy cập bằng GET
    return render_template('add_product.html')
@app.route('/list_product')
def list_product():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM product ORDER BY id DESC")
    
    product = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('list_product.html', product=product)
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE product SET name=%s, price=%s WHERE id=%s", (name, price, id)
        )
        
        conn.commit()
        
        cur.close()
        conn.close()
        
        return redirect('/list_product')
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM product WHERE id=%s", (id,))
    product = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return render_template('edit_product.html', product=product)
@app.route('/delete_product/<int:id>')
def delete_product(id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM product WHERE id=%s", (id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    return redirect('/list_product')
if __name__ == '__main__':
    app.run(debug=True)
        