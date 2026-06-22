key = ['name', 'age', 'city']
value = ['quang', 21, 'Da Nang']
thong_tin = {}
for i in range(len(key)):
    thong_tin[key[i]] = value[i]
print(thong_tin)

student = {'name': 'quang', 'age': 21, 'city': 'Da Nang'}
print(student['name'])
student["grade"] = "A"
student["age"] = 22
for key, value in student.items():
    print(f"{key}: {value}")

# Bài 1: Tạo một từ điển chứa tên và tuổi của ba người, sau đó in ra thông tin của từng người.​
people = {
    'Alice': 30,
    'Bob': 25,
    'Charlie': 35
}
for name, age in people.items():
    print(f"{name} is {age} years old.")

# Bài 2: Viết chương trình nhận vào một dictionary chứa tên sinh viên và điểm số của họ, sau đó trả về danh sách các sinh viên có điểm lớn hơn hoặc bằng 8.​

def high_achievers(students):
   achievers = {name: score for name, score in students.items() if score >= 8}
   return achievers

student_scores = {
   "Alice": 9,
   "Bob": 7.5,
   "Charlie": 8,
   "David": 6.5,
   "Eva": 8.5
}
result = high_achievers(student_scores)
print(result)  # Output: ['Alice', 'Charlie', 'Eva']
