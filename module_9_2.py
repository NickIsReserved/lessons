first_strings = ['Elon', 'Musk', 'Programmer', 'Monitors', 'Variable']
second_strings = ['Task', 'Git', 'Comprehension', 'Java', 'Computer', 'Assembler']

# 1. Список длины строк списка first_strings, если длина строки >= 5
first_result = [len(s) for s in first_strings if len(s) >= 5]

# 2. Список кортежей слов одинаковой длины из списков first_strings и second_strings
second_result = [(s1, s2) for s1 in first_strings for s2 in second_strings if len(s1) == len(s2)]

# 3. Словарь со строками чётной длины и их длиной из объединённых списков
third_result = {s: len(s) for s in first_strings + second_strings if len(s) % 2 == 0}

# Пример выполнения кода
print(first_result)
print(second_result)
print(third_result)
