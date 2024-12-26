import inspect
from typing import Any, Dict, List, TypedDict


class IntrospectionInfo(TypedDict):
    type: str
    module: str
    attributes: List[str]
    methods: List[str]
    additional_info: Dict[str, Any]


def introspection_info(obj: Any) -> IntrospectionInfo:
    info: IntrospectionInfo = {
        'type': type(obj).__name__,
        'module': inspect.getmodule(obj).__name__ if inspect.getmodule(
            obj) else getattr(obj, '__class__', obj).__module__,
        'attributes': [],
        'methods': [],
        'additional_info': {}
    }

    # Получаем список всех атрибутов объекта
    attributes = dir(obj)

    # Разделяем атрибуты на методы и обычные атрибуты
    info['attributes'] = [attr for attr in attributes if not callable(
        getattr(obj, attr, None)) and not attr.startswith('__')]
    info['methods'] = [method for method in attributes if callable(
        getattr(obj, method, None)) and not method.startswith('__')]

    # Дополнительная информация в зависимости от типа объекта
    if isinstance(obj, (int, float, complex)):
        info['additional_info'] = {
            'is_integer': isinstance(obj, int),
            'is_real': isinstance(obj, (int, float)),
            'absolute_value': abs(obj)
        }
    elif isinstance(obj, str):
        info['additional_info'] = {
            'length': len(obj),
            'is_alphanumeric': obj.isalnum(),
            'is_uppercase': obj.isupper(),
            'is_lowercase': obj.islower()
        }
    elif isinstance(obj, list):
        info['additional_info'] = {
            'length': len(obj),
            'is_empty': len(obj) == 0
        }
    elif isinstance(obj, dict):
        info['additional_info'] = {
            'length': len(obj),
            'keys': list(obj.keys()),
            'is_empty': len(obj) == 0
        }
    elif inspect.isfunction(obj):
        info['additional_info'] = {
            'function_name': obj.__name__,
            'module': obj.__module__,
            'arguments': list(inspect.signature(obj).parameters.keys())
        }
    elif inspect.isclass(obj):
        info['additional_info'] = {
            'class_name': obj.__name__,
            'module': obj.__module__,
            'bases': [b.__name__ for b in obj.__bases__],
            'class_methods': [name for name, method in
                              inspect.getmembers(obj, inspect.isfunction) if
                              inspect.ismethod(
                                  method) or method.__qualname__.startswith(
                                  obj.__name__)],
            'static_methods': [name for name, method in
                               inspect.getmembers(obj, inspect.isfunction) if
                               method.__qualname__.startswith(
                                   obj.__name__ + '.') and not inspect.ismethod(
                                   method)]
        }

    return info


# Примеры использования
def example_usage():
    # Интроспекция числа
    number_info = introspection_info(42)
    print("\nИнформация о числе:")
    for k, v in number_info.items():
        print(f'{k}: {v}')

    # Интроспекция строки
    string_info = introspection_info("Hello, World!")
    print("\nИнформация о строке:")
    for k, v in string_info.items():
        print(f'{k}: {v}')

    # Интроспекция списка
    list_info = introspection_info([1, 2, 3, 4])
    print("\nИнформация о списке:")
    for k, v in list_info.items():
        print(f'{k}: {v}')

    # Интроспекция функции
    def example_func(x, y):
        return x + y

    function_info = introspection_info(example_func)
    print("\nИнформация о функции:")
    for k, v in function_info.items():
        print(f'{k}: {v}')

    # Интроспекция класса
    class ExampleClass:
        def __init__(self, value):
            self.value = value

        def method(self):
            return self.value * 2

        @classmethod
        def class_method(cls):
            return "This is a class method"

        @staticmethod
        def static_method():
            return "This is a static method"

    class_info = introspection_info(ExampleClass)
    print("\nИнформация о классе:")
    for k, v in class_info.items():
        print(f'{k}: {v}')


if __name__ == "__main__":
    example_usage()
