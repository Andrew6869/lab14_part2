#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Перемножение матриц с использованием multiprocessing.Pool

Основа — функция element() из репозитория:
https://github.com/fa-python-network/3_Parallelism

Задания:
  TODO 3 — использовать Pool.starmap() для параллельного вычисления
  TODO 4 — запустить с разным числом процессов (1, 2, 4) и сравнить время

Запуск:
    python3 03_pool_matrix.py
"""

import time
import random
from multiprocessing import Pool

def init_matrix(rows, cols):
    """Создаёт матрицу rows×cols со случайными значениями."""
    return [[random.random() for _ in range(cols)] for _ in range(rows)]

def element(i, j, A, B):
    """
    Вычисляет один элемент результирующей матрицы.
    i, j — индексы элемента
    A, B — исходные матрицы
    """
    N = len(A[0])  # количество столбцов A = количество строк B
    res = sum(A[i][k] * B[k][j] for k in range(N))
    return (i, j, res)

if __name__ == "__main__":
    # Размеры матриц: A (M×N), B (N×K) → результат M×K
    M, N, K = 100, 100, 100

    print(f"Инициализация матриц {M}x{N} и {N}x{K}...")
    A = init_matrix(M, N)
    B = init_matrix(N, K)

    # ------------------------------------------------------------
    # Последовательное вычисление (baseline)
    # ------------------------------------------------------------
    print("\n--- Последовательное вычисление ---")
    start_seq = time.time()

    C_seq = [[0] * K for _ in range(M)]
    for i in range(M):
        for j in range(K):
            C_seq[i][j] = sum(A[i][k] * B[k][j] for k in range(N))

    seq_time = time.time() - start_seq
    print(f"Время: {seq_time:.4f} сек")

    # ------------------------------------------------------------
    # TODO 3: Параллельное вычисление с Pool.starmap()
    # TODO 4: Запуск с разным количеством процессов в пуле (1, 2, 4)
    # ------------------------------------------------------------
    
    # Подготавливаем аргументы для каждого элемента
    args = [(i, j, A, B) for i in range(M) for j in range(K)]
    
    pool_sizes = [1, 2, 4]
    
    for pool_size in pool_sizes:
        print(f"\n--- Параллельное вычисление (Pool, процессов={pool_size}) ---")
        start_par = time.time()
        
        # Создаём пул процессов
        with Pool(processes=pool_size) as pool:
            # starmap распаковывает каждый кортеж из args в отдельные аргументы
            results = pool.starmap(element, args)
        
        # Собираем результаты в матрицу
        C_par = [[0] * K for _ in range(M)]
        for i, j, value in results:
            C_par[i][j] = value
        
        par_time = time.time() - start_par
        
        # Проверка корректности
        correct = True
        for i in range(M):
            for j in range(K):
                if abs(C_seq[i][j] - C_par[i][j]) > 1e-10:
                    correct = False
                    break
            if not correct:
                break
        
        print(f"Время: {par_time:.4f} сек")
        print(f"Ускорение: {seq_time/par_time:.2f}x")
        print(f"Результаты {'совпадают' if correct else 'НЕ совпадают'}")
