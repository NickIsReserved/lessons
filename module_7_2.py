def custom_write(file_name, strings):
    strings_positions = {}
    try:
        file = open(file_name, 'w', encoding='utf-8')
        for i, string in enumerate(strings, start=1):
            pos = file.tell()
            file.write(string + '\n')
            strings_positions[(i, pos)] = string
        file.close()
        return strings_positions
    except IOError as e:
        print(f"Ошибка создания файла: {e}")


# Пример использования
info = [
    'Text for tell.',
    'Используйте кодировку utf-8.',
    'Because there are 2 languages!',
    'Спасибо!'
]

result = custom_write('test.txt', info)
for elem in result.items():
    print(elem)
