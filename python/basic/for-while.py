for i in range(5):
    print("Lần lặp thứ:", i)

count = 0
while count < 5:
    count += 1
    print("Đếm:", count)
    
for i in range(10):
    if i == 5:
        break  # Dừng vòng lặp khi i bằng 5
    print(i)

for i in range(10):
    if i % 2 == 0:
        continue  # Bỏ qua các số chẵn
    print(i)
    
# In ra các số từ 1 đến 10, nhưng bỏ qua số 5
for i in range(1, 11):
    if i == 5:
        continue
    print(i)