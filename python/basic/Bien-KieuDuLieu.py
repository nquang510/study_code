x = 10 #Kiểu int
y = 3.14 #Kiểu float
name = "Alice" #Kiểu str
is_student = True #Kiểu bool

my_list = [1, 2, 3, 4, 5] #Kiểu list
my_tuple = (1, 2, 3) #Kiểu tuple
my_dict = {"name": "Alice", "age": 25} #Kiểu dict
my_set = {1, 2, 3} #Kiểu set

#Viết 1 chương trình yêu cầu nhập vào một số nguyên và một số thực sau đó in ra màn hình kiểu dữ liệu của chúng
num_int = int(input("Nhập vào một số nguyên: "))
num_float = float(input("Nhập vào một số thực: "))
print("Kiểu dữ liệu của số nguyên là:", type(num_int))
print("Kiểu dữ liệu của số thực là:", type(num_float))