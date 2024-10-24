def test_function():
    def inner_function():
        print("Я в области видимости функции test_function")

    inner_function()


test_function() # Вывод: Я в области видимости функции test_function
"""
Попытка вызывать inner_function вне функции test_function вызывает ошибку:
# NameError: name 'inner_function' is not defined.
"""
inner_function()
