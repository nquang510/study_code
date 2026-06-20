numbers = []
for i in range(1, 6):
    numbers.append(i)
print(numbers)
tuple_numbers = tuple(numbers)
print(tuple_numbers)

fruits = ('apple', 'banana', 'cherry')
for fruit in fruits:
    print(fruit)

# Viết chương trình nhận vào một tuple chứa các số nguyên và trả về một tuple mới chứa các phần tử là bội số của 3​
def multiples_of_three(numbers):
    multiples = tuple(num for num in numbers if num % 3 == 0)
    return multiples
tuple_input = (1, 2, 3, 4, 5, 6, 7, 8, 9)
tuple_output = multiples_of_three(tuple_input)
print(tuple_output)
    
