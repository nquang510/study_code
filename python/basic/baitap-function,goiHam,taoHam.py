#Bài 1: Viết hàm nhập vào 1 số và kiêm tra đó là số chẵn hay lẽ và in ra màn hình số đó
def kiem_tra_chan_le():
   #try-except để xử lý lỗi khi người dùng nhập không phải là số nguyên
   try:
       so = int(input("Nhập một số nguyên: "))
       if so % 2 == 0:
           print(f"{so} là số chẵn.")
       else:
           print(f"{so} là số lẻ.")
   except ValueError:
       print("Vui lòng nhập một số nguyên hợp lệ.")
kiem_tra_chan_le()

#Bài 2: Viết hàm nhập vào 2 số, tính tổng 2 số đó và in ra màn hinh.
def tinh_tong_hai_so():
   try:
       number1 = float(input("Nhập số thứ nhất: "))
       number2 = float(input("Nhập số thứ hai: "))
       tong = number1 + number2
       print(f"Tổng của {number1} và {number2} là: {tong}")
   except ValueError:
       print("Vui lòng nhập vào một số hợp lệ.")
tinh_tong_hai_so()

#Bài 3: Viết 1 chương trình nhập vào 3 số, số cuối cùng là true hoặc false. Nêu true thi làm phép tính tổng 2 số đầu tiên Nếu flase thi làm phép tính nhân 2 số đầu tiên. và tách phần tỉnh tổng và tính nhân ra 2 hàm riêng, gọi 2 hàm đó vào trong hàm nhập 3 số. Sau đó in ra màn hình kết quả.
def tinh_tong(a, b):
   return a + b
def tinh_nhan(a, b):
   return a * b
def nhap_va_tinh():
   try:
       so_thu_nhat = float(input("Nhập số thứ nhất: "))
       so_thu_hai = float(input("Nhập số thứ hai: "))
       lua_chon = input("Nhập giá trị True hoặc False: ").strip().capitalize()
       if lua_chon not in ["True", "False"]:
           raise ValueError("Giá trị boolean không hợp lệ.")
       lua_chon = lua_chon == "True"
       if lua_chon:
           ket_qua = tinh_tong(so_thu_nhat, so_thu_hai)
           phep_tinh = "tổng"
       else:
           ket_qua = tinh_nhan(so_thu_nhat, so_thu_hai)
           phep_tinh = "tích"
       print(f"{phep_tinh.capitalize()} của {so_thu_nhat} và {so_thu_hai} là: {ket_qua}")
   except ValueError as e:
       print(f"Lỗi: {e}. Vui lòng nhập lại dữ liệu hợp lệ.")
nhap_va_tinh()

