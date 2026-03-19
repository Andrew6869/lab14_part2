#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Сравнение синхронного и асинхронного подходов для IO-bound задач.
"""

import time
import asyncio

# ------------------------------------------------------------
# Синхронная версия (блокирующая)
# ------------------------------------------------------------
def fetch_data_sync(source, delay):
    """Имитация долгого IO-запроса (блокирующая)."""
    print(f"  Запрос к '{source}'...")
    time.sleep(delay)  # блокирует весь поток
    print(f"  Ответ от '{source}' получен")
    return f"данные из {source}"

def main_sync():
    """Синхронное выполнение трёх запросов."""
    print("\n--- Синхронное выполнение ---")
    start = time.time()

    results = []
    results.append(fetch_data_sync("API сервер", 2))
    results.append(fetch_data_sync("База данных", 3))
    results.append(fetch_data_sync("Файловое хранилище", 1))

    elapsed = time.time() - start
    print(f"\nРезультаты: {results}")
    print(f"Время выполнения: {elapsed:.2f} сек")
    return elapsed, results

# ------------------------------------------------------------
# Асинхронная версия (неблокирующая)
# ------------------------------------------------------------
async def fetch_data_async(source, delay):
    """Имитация долгого IO-запроса (неблокирующая)."""
    print(f"  Запрос к '{source}'...")
    await asyncio.sleep(delay)  # не блокирует поток
    print(f"  Ответ от '{source}' получен")
    return f"данные из {source}"

# TODO 5: Допишите асинхронную версию с использованием asyncio.gather()
async def main_async():
    """Асинхронное выполнение трёх запросов."""
    print("\n--- Асинхронное выполнение ---")
    start = time.time()
    
    # Запускаем все три корутины одновременно
    results = await asyncio.gather(
        fetch_data_async("API сервер", 2),
        fetch_data_async("База данных", 3),
        fetch_data_async("Файловое хранилище", 1)
    )
    
    elapsed = time.time() - start
    print(f"\nРезультаты: {results}")
    print(f"Время выполнения: {elapsed:.2f} сек")
    return elapsed, results

# ------------------------------------------------------------
# Запуск
# ------------------------------------------------------------
if __name__ == "__main__":
    sync_time, sync_results = main_sync()
    
    # Запускаем асинхронную функцию
    async_time, async_results = asyncio.run(main_async())
    
    print(f"\n--- Сравнение ---")
    print(f"Синхронно: {sync_time:.2f} сек, результаты: {sync_results}")
    print(f"Асинхронно: {async_time:.2f} сек, результаты: {async_results}")
    print(f"Асинхронно быстрее в {sync_time/async_time:.2f} раза")
