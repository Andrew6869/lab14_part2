#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простой TCP-клиент для тестирования многопроцессного сервера.
Можно запускать несколько экземпляров в разных терминалах.
"""

import socket
import time
import sys

HOST = '127.0.0.1'
PORT = 9090  # Изменено с 9095 на 9090

def run_client(client_id=1):
    """Подключается к серверу, отправляет сообщение и получает ответ."""
    try:
        # Создаём сокет
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        # Формируем сообщение
        message = f"Привет от клиента #{client_id}! Время: {time.strftime('%H:%M:%S')}"
        print(f"[Клиент {client_id}] Отправка: '{message}'")

        # Отправляем данные
        client.send(message.encode())

        # Получаем ответ
        response = client.recv(1024).decode()
        print(f"[Клиент {client_id}] Получено: '{response}'")

        # Закрываем соединение
        client.close()
        return True

    except ConnectionRefusedError:
        print(f"[Клиент {client_id}] Ошибка: не удалось подключиться к серверу.")
        print("Убедитесь, что сервер 04_mp_echo_server.py запущен в другом терминале.")
        return False
    except Exception as e:
        print(f"[Клиент {client_id}] Ошибка: {e}")
        return False

if __name__ == "__main__":
    # Получаем ID клиента из аргументов командной строки, если передан
    client_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_client(client_id)
