from flask import Flask, render_template

app = Flask(__name__)

# Route cho trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Route cho trang giỏ hàng
@app.route('/cart')
def cart():
    return render_template('cart.html')

# Route cho trang blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(debug=True)