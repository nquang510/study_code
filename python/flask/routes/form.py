from flask import Blueprint, render_template, request, session, redirect, url_for
form_bp = Blueprint('form', __name__)
@form_bp.route('/form', methods=['GET', 'POST'])
def form():
    errors = {}
    email = request.form.get('email','').strip()
    password = request.form.get('password','').strip()
    city = request.form.get('city','').strip()
    if request.method == 'POST':
        if not email:
            errors['email'] = 'Vui lòng nhập Email'
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu'
        if not city:
            errors['city'] = 'Vui lòng nhập thành phố'
        if not errors:
            new_entry = {
                'email': email,
                'password': password,
                'city': city
            }
            if 'form' not in session:
                session['form'] = []
                session['form'].append(new_entry)
                session.modified = True # Để flask nhận ra session đã thay đổi
                return redirect(url_for('form.table'))
    return render_template('form.html', errors=errors, email=email, password=password, city=city)
@form_bp.route('/table')
def table():
    session_data = session.get('form', [])
    return render_template('table.html', session_data=session_data)