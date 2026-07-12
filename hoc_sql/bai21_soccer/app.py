from flask import Flask, render_template, request, redirect
from db import get_connection

app = Flask(__name__)

@app.route('/add_soccer', methods=['GET', 'POST'])
def add_soccer():
    if request.method == 'POST':
        #Lấy dữ liệu từ form
        tenCauThu = request.form['tenCauThu']
        tuoi = request.form['tuoi']
        quocTich = request.form['quocTich']
        viTri = request.form['viTri']
        luong = request.form['luong']
        
        #Kết nối mysql
        conn = get_connection()
        cur = conn.cursor()

        #Insert dữ liệu
        cur.execute(
            "INSERT INTO soccer (tenCauThu, tuoi, quocTich, viTri, luong) VALUES (%s, %s, %s, %s, %s)", (tenCauThu, tuoi, quocTich, viTri, luong)
        )
        
        #Lưu dữ liệu xuống db
        conn.commit()
        
        #Đóng kết nối
        cur.close()
        conn.close()
        
        #Sau khi xong quay lại trang add_product
        return redirect('/add_soccer')
    #Nếu người dùng truy cập bằng GET
    return render_template('add_soccer.html')
@app.route('/list_soccer')
def list_soccer():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM soccer ORDER BY id DESC")
    
    soccer = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('list_soccer.html', soccer=soccer)
@app.route('/edit_soccer/<int:id>', methods=['GET', 'POST'])
def edit_soccer(id):
    if request.method == 'POST':
        tenCauThu = request.form['tenCauThu']
        tuoi = request.form['tuoi']
        quocTich = request.form['quocTich']
        viTri = request.form['viTri']
        luong = request.form['luong']
        
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute(
            "UPDATE soccer SET tenCauThu=%s, tuoi=%s, quocTich=%s, viTri=%s, luong=%s WHERE id=%s", (tenCauThu, tuoi, quocTich, viTri, luong, id)
        )
        
        conn.commit()
        
        cur.close()
        conn.close()
        
        return redirect('/list_soccer')
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM soccer WHERE id=%s", (id,))
    soccer = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return render_template('edit_soccer.html', soccer=soccer)
@app.route('/delete_soccer/<int:id>')
def delete_soccer(id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM soccer WHERE id=%s", (id,))
    conn.commit()
    
    cur.close()
    conn.close()
    
    return redirect('/list_soccer')
if __name__ == '__main__':
    app.run(debug=True)
        