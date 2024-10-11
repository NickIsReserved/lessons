""" Основное решение:
    Если число заканчивается на 0, умножаем на 0
"""
def get_multiplied_digits(number: int):
    str_number = str(number)
    first = int(str_number[0])
    if len(str_number) > 1:
        first = first * get_multiplied_digits(int(str_number[1:]))

    return first


""" Дополнительное решение:
    Если число заканчивается на 0, не умножаем на 0, выходим из цикла
"""
def get_multiplied_digits_zero_check(number: int):
    str_number = str(number)
    first = int(str_number[0])
    if len(str_number) > 1:
        zero_check = int(str_number[1:])
        if zero_check != 0:
            first = first * get_multiplied_digits_zero_check(zero_check)

    return first


result = get_multiplied_digits(40203)
print(result)
result = get_multiplied_digits(402030)
print(result, '\n')
result = get_multiplied_digits_zero_check(40203)
print(result)
result = get_multiplied_digits_zero_check(402030)
print(result)

