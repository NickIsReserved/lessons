class Product:
    def __init__(self, name: str, weight: float, category: str):
        self.name = name
        self.weight = weight
        self.category = category

    def __str__(self):
        return f"{self.name}, {self.weight}, {self.category}"


class Shop:
    __file_name = 'products.txt'

    def get_products(self):
        try:
            file = open(self.__file_name, 'r')
            data = file.read()
            file.close()
            return data
        except FileNotFoundError:
            self.__create_file()
            return "Файл создан."
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")

    def add(self, *products):
        existing_products = self.get_products().splitlines()
        existing_names = [line.split(',')[0].strip() for line in
                          existing_products]
        try:
            file = open(self.__file_name, 'a')
            for product in products:
                product_name = product.name
                if product_name in existing_names:
                    print(
                        f"Продукт {product.name}, {product.weight}, "
                        f"{product.category} уже есть в магазине")
                else:
                    file.write(str(product) + '\n')
            file.close()
        except IOError as e:
            print(f"Ошибка добавления: {e}")

    def __create_file(self):
        try:
            file = open(self.__file_name, 'w')
            file.close()
        except IOError as e:
            print(f"Ошибка создания файла: {e}")


s1 = Shop()
p1 = Product('Potato', 50.5, 'Vegetables')
p2 = Product('Spaghetti', 3.4, 'Groceries')
p3 = Product('Potato', 5.5, 'Vegetables')

print(p2)  # Spaghetti, 3.4, Groceries

s1.add(p1, p2, p3)

print(s1.get_products())
