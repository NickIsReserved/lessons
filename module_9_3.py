first = ['Strings', 'Student', 'Computers']
second = ['Строка', 'Урбан', 'Компьютер']

# 1. Генераторная сборка, которая вычисляет разницу длин строк, если их длины не равны
first_result = (abs(len(f) - len(s)) for f, s in zip(first, second) if len(f) != len(s))

# 2. Генераторная сборка, которая сравнивает длины строк в одинаковых позициях (без zip)
second_result = (len(first[i]) == len(second[i]) for i in range(len(first)))

# Пример выполнения кода:
print(list(first_result))
print(list(second_result))
