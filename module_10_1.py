from threading import Thread
from time import sleep
from time import time


def write_words(word_count, file_name):
    """
    Функция записывает указанное количество слов в файл с паузой 0.1 секунды
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for i in range(1, word_count + 1):
            file.write(f'Какое-то слово № {i}\n')
            sleep(0.1)

    print(f'Завершилась запись в файл {file_name}')


def main():
    # Измерение времени выполнения функций
    start_functions = time()

    # Вызов функций
    write_words(10, 'example1.txt')
    write_words(30, 'example2.txt')
    write_words(200, 'example3.txt')
    write_words(100, 'example4.txt')

    end_functions = time()
    print(f'Работа функций {end_functions - start_functions:.2f} секунд')

    # Измерение времени работы потоков
    start_threads = time()

    # Создание потоков
    threads = [
        Thread(target=write_words, args=(10, 'example5.txt')),
        Thread(target=write_words, args=(30, 'example6.txt')),
        Thread(target=write_words, args=(200, 'example7.txt')),
        Thread(target=write_words, args=(100, 'example8.txt'))
    ]

    # Запуск потоков
    for thread in threads:
        thread.start()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    end_threads = time()
    print(f'Работа потоков {end_threads - start_threads:.2f} секунд')


if __name__ == '__main__':
    main()
