def apply_all_func(int_list, *functions):
    results = {}

    for func in functions:
        """ Применяем функцию к int_list и записываем результат в словарь """
        results[func.__name__] = func(int_list)

    return results


# Пример работы кода:
print(apply_all_func([6, 20, 15, 9], max, min))
print(apply_all_func([6, 20, 15, 9], len, sum, sorted))
