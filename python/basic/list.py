numbers = [1, 2, 3, 4, 5]
print(numbers[0])  # Truy cập phần tử đầu tiên
numbers.append(6)  # Thêm phần tử vào cuối danh sách
numbers.insert(2, 10)  # Chèn số 10 vào vị trí 2
numbers.remove(10) # Xóa phần tử có giá trị 10

for num in numbers:
    print(num)

list = []
for i in range(1, 6):
    list.append(i)
print(list)

#Duyệt mảng bằng for-range
list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in range(len(list1)):
   print(f"Phần tử thứ {i} là: {list1[i]}")

#Duyệt mảng bằng while
list2 = [1, 2, 3, 4, 5]  
i = 0
while i < len(list2):
    print(f"Phần tử thứ {i} là: {list2[i]}")
    i += 1

#Duyệt mảng bẳng enumerate
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits):
    print(f"Phần tử thứ {index} là: {fruit}")
    
#Duyệt mảng bằng list comprehension
numbers = [1, 2, 3, 4, 5]
squared_numbers = [num ** 2 for num in numbers] #Bình phương các phần tử trong mảng
print(squared_numbers)

#Các cách xóa phần tử trong mảng
my_list = [1, 2, 3, 4, 5]
my_list.remove(3)  # Xóa phần tử có giá trị 3
my_list.pop(1)  # Xóa phần tử tại vị trí 1 (số 2)
del my_list[0]  # Xóa phần tử tại vị trí 0 (số 1)
my_list.clear()  # Xóa tất cả phần tử trong mảng
print(my_list)  # In ra mảng sau khi xóa

#Bài 1: Viết chương trình dùng for tạo 1 mảng từ 1 - 10 sau đó duyệt mảng và in ra các số chẵn
numbers = []
for i in range(1, 11):
    numbers.append(i)
for num in numbers:
    if num % 2 == 0:
        print(num)

#Bài 2: Cho 1 mảng bất kỳ dùng for tìm số lớn nhất trong mảng
list = [10, 7, 13, 5, 2]
max_num = list[0]
for num in list:
    if num > max_num:
        max_num = num
print("Số lớn nhất trong mảng là:", max_num)

max_num = max(list)
print("Số lớn nhất trong mảng là:", max_num)

#Bài 3: Cho chuỗi "Quang" dùng for duyệt chuỗi và in ra từng ký tự
name = "Quang"
for char in name:
    print(char)

#Bài 4: Vòng lặp for tính tổng theo công thức sau: S = 1 + 1/2 + 1/3 + ... + 1/n
n = int(input("Nhập vào số n: "))
S = 0
for i in range(1, n + 1):
    S += 1 / i
print("Tổng là:", S)
