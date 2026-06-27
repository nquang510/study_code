from flask import Flask, render_template

app = Flask(__name__)
def generate_students(count):
    students = []
    for i in range(1, count + 1):
        student= {
            'name': f'Nguyen Phan Nhat Quang {i}',
            'email': f'nhatquang{i}@gmail.com',
            'age': 20
        }
        students.append(student)
    return students

@app.route('/')
def home():
    numbers = list(range(1, 11))
    return render_template('index.html', numbers=numbers)
@app.route('/students')
def students():
    students_list = generate_students(10)
    return render_template('students.html', students=students_list)
# Bài tập 1: Tìm các số chẵn trong mảng
@app.route('/evenNumber')
def evenNumber():
    numbers = list(range(1, 101))
    even_numbers = [value for value in numbers if value % 2 == 0]
    return render_template('evenNumber.html', numbers=even_numbers)
# Bài tập 2: Tìm số lớn nhất trong mảng
@app.route('/maxNumber')
def maxNumber():
    numbers = [1, 23, 32, 5, 43, 321, 312, 352, 2, 13, 153, 21, 32, 1];
    for value in numbers:
        if value == max(numbers):
            max_number = value
    return render_template('maxNumber.html', max_number=max_number)
# Bài tập 3: Giả sử có chuỗi $name = "Nguyen Phan Nhat Quang", sử dụng vòng lặp for để in ra từng ký tự trong chuỗi
@app.route('/printName')
def printName():
    name = "Nguyen Phan Nhat Quang"
    characters = [char for char in name]
    return render_template('printName.html', characters=characters)
#Bài tập 4: Vòng lặp for tính tổng S= 1 + 1/2 + 1/3 + 1/4 + ... + 1/n 
@app.route('/sum1')
def sum1():
    n = 2
    total_sum1 = sum(1/i for i in range(1, n + 1))
    return render_template('sum1.html', total_sum1=total_sum1)
# Bài tập 5: Vòng lặp for tính tổng S= x*2 + x*4 + x*6 + ... + x*2n
@app.route('/sum2')
def sum2():
    x = 2
    n = 3
    total_sum2 = sum(x * i for i in range(2, 2 * n + 1, 2))
    return render_template('sum2.html', total_sum2=total_sum2)
# Bài tập 6: Vòng lặp for bước nhảy 2
@app.route('/forStep')
def forStep():
    numbers = list(range(1, 101, 2))
    return render_template('forStep.html', numbers=numbers)

if __name__ == '__main__':
    app.run(debug=True)