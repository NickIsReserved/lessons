from time import time
from multiprocessing import Pool
from typing import List


def read_info(name: str) -> None:
    all_data = []
    with open(name, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            all_data.append(line)


def linear_processing(filenames_list: List[str]) -> None:
    """Линейный вызов"""
    start_time = time()
    for filename in filenames_list:
        read_info(filename)
    print(f"{time() - start_time:.2f} сек. (линейный)")


def multi_processing(filenames_list: List[str]) -> None:
    """Многопроцессный вызов"""
    start_time = time()
    with Pool() as pool:
        pool.map(read_info, filenames_list)
    print(f"{time() - start_time:.2f} сек. (многопроцессный)")


if __name__ == '__main__':
    filenames = [f'./file {number}.txt' for number in range(1, 5)]

    """Линейный вызов"""
    linear_processing(filenames)
    """Многопроцессный"""
    # multi_processing(filenames)
