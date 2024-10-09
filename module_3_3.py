def print_params(a=1, b='строка', c=True):
    print(a, b, c)


print("Функция:\ndef print_params(a=1, b='строка', c=True):\n    print(a, b, c)")
print('Выводим print_params()')
print_params()
print('Выводим print_params(b=25)')
print_params(b=25)
print('Выводим print_params(c=[1, 2, 3])')
print_params(c=[1, 2, 3])

empty_list = []  # пустой список
print('Пытаемся вывести empty_list, проверяем, что список не пуст')
print_params(*empty_list if empty_list else {})  # проверка, что список не пуст

print('Выводим values_list = [2, "список", False]')
values_list = [2, 'список', False]
print_params(*values_list)

print("Выводим values_dict = {'a': 3.0, 'b': 'словарь', 'c': False}")
values_dict = {'a': 3.0, 'b': 'словарь', 'c': False}
print_params(**values_dict)

print("Выводим values_list_2 = [54.32, 'Строка']")
values_list_2 = [54.32, 'Строка']
print_params(*values_list_2, 42)
