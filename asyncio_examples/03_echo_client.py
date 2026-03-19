#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Асинхронный эхо-клиент для сервера из задания B2
(на основе https://github.com/fa-python-network/4_asyncio_server)
"""

import asyncio
import time

HOST = '127.0.0.1'
PORT = 9095

# TODO 7: Дописать отправку сообщения и получение ответа
async def tcp_echo_client(message, client_id=1):
    """
    Подключается к серверу, отправляет сообщение и получает ответ.
    message: строка для отправки
    client_id: идентификатор клиента для логов
    """
    print(f"[Клиент {client_id}] Подключение к {HOST}:{PORT}...")
    
    try:
        # Устанавливаем соединение с сервером
        reader, writer = await asyncio.open_connection(HOST, PORT)
        
        # Отправляем сообщение
        data = message.encode()
        writer.write(data)
        await writer.drain()
        print(f"[Клиент {client_id}] Отправлено: '{message}'")
        
        # Читаем ответ от сервера
        response = await reader.read(1024)
        response_str = response.decode()
        print(f"[Клиент {client_id}] Получено: '{response_str}'")
        
        # Закрываем соединение
        writer.close()
        await writer.wait_closed()
        
        return response_str
        
    except ConnectionRefusedError:
        print(f"[Клиент {client_id}] Ошибка: сервер не доступен. Запустите сервер сначала!")
        return None
    except Exception as e:
        print(f"[Клиент {client_id}] Ошибка: {e}")
        return None

# TODO 8: Запустить несколько клиентов одновременно через gather()
async def main():
    """Запуск нескольких клиентов одновременно."""
    print("=== Тестирование асинхронного эхо-клиента ===\n")
    
    # Сначала проверим одного клиента
    print("--- Один клиент ---")
    result = await tcp_echo_client("Привет, сервер!", 1)
    print(f"Результат одного клиента: {result}\n")
    
    # Теперь запустим несколько клиентов одновременно
    print("--- Несколько клиентов одновременно ---")
    
    # Создаём список сообщений для разных клиентов
    messages = [
        "Привет от первого клиента!",
        "Hello from second client!",
        "Bonjour du troisième client!",
        "Ciao dal quarto cliente!",
        "Hallo vom fünften Klienten!"
    ]
    
    # Создаём задачи для всех клиентов
    tasks = []
    for i, msg in enumerate(messages, 1):
        task = tcp_echo_client(msg, i)
        tasks.append(task)
    
    # Запускаем все клиенты одновременно и замеряем время
    start = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    
    print(f"\n--- Все клиенты завершили работу за {elapsed:.2f} сек ---")
    print(f"Получено ответов: {len([r for r in results if r is not None])}")
    
    # Выводим все результаты
    print("\n--- Полученные ответы ---")
    for i, result in enumerate(results, 1):
        print(f"Клиент {i}: {result}")
    
if __name__ == '__main__':
    asyncio.run(main())
