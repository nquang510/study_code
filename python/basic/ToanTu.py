a = 10
b = 3

print(a + b)  # Cộng
print(a - b)  # Trừ
print(a * b)  # Nhân
print(a / b)  # Chia
print(a % b)  # Chia lấy dư
print(a // b) # Chia lấy phần nguyên
print(a ** b) # Lũy thừa


print(a == b)  # So sánh bằng
print(a != b)  # Khác nhau
print(a > b)   # Lớn hơn
print(a < b)   # Nhỏ hơn
print(a >= b)  # Lớn hơn hoặc bằng
print(a <= b)  # Nhỏ hơn hoặc bằng

#Viết chương trình nhập vào 2 số a và b sau đó in ra kết quả của các phép toán trên
a = int(input("Nhập vào số a: "))
b = int(input("Nhập vào số b: "))
print(a + b, a - b, a * b, a / b, a % b, a // b, a ** b)