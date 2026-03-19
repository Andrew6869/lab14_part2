#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Многопроцессный эхо-сервер (каждый клиент обрабатывается в отдельном процессе)
Аналог многопоточного сервера из лабораторной работы 2, но с multiprocessing.

Основа — репозиторий: https://github.com/fa-python-network/2_threaded_server
(там threading, мы переделываем на multiprocessing)

Задания:
  TODO 9 — реализовать функцию handle_client (приём данных, логирование, отправка)

Запуск:
    python3 04_mp_echo_server.py

Для проверки используйте готовый клиент 05_mp_echo_client.py в другом терминале
или несколько терминалов с ним.
"""

import socket
import os
import signal
import sys
from multiprocessing import Process

# TODO 9: Реализовать тело функции handle_client
def handle_client(client_socket, client_addr):
    """
    Обрабатывает одного клиента в отдельном процессе.
    client_socket: сокет для общения с клиентом
    client_addr: адрес клиента (ip, port)
    """
    pid = os.getpid()
    ppid = os.getppid()

    print(f"[PID {pid}] Начало обработки клиента {client_addr} (родительский PID: {ppid})")

    try:
        # Получаем данные от клиента (максимум 1024 байта)
        data = client_socket.recv(1024)
        if not data:
            print(f"[PID {pid}] Клиент {client_addr} закрыл соединение без отправки данных")
            return

        message = data.decode()
        print(f"[PID {pid}] Получено от {client_addr}: '{message}'")

        # Отправляем данные обратно клиенту (эхо)
        client_socket.send(data)
        print(f"[PID {pid}] Отправлено клиенту {client_addr}: '{message}'")

    except ConnectionResetError:
        print(f"[PID {pid}] Соединение с {client_addr} сброшено")
    except Exception as e:
        print(f"[PID {pid}] Ошибка при обработке {client_addr}: {e}")
    finally:
        # Закрываем соединение с клиентом
        client_socket.close()
        print(f"[PID {pid}] Соединение с {client_addr} закрыто, процесс завершается")

def start_server(host='127.0.0.1', port=9090):
    """
    Запускает многопроцессный сервер.
    Главный процесс принимает подключения и для каждого создаёт дочерний процесс.
    """
    # Игнорируем SIGCHLD, чтобы зомби-процессы автоматически удалялись
    # (на некоторых Unix-системах)
    try:
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    except AttributeError:
        # Windows не поддерживает SIGCHLD
        pass

    # Создаём сокет
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)

    print(f"Многопроцессный эхо-сервер запущен на {host}:{port}")
    print(f"Главный процесс PID: {os.getpid()}")
    print("Ожидание подключений... (Ctrl+C для остановки)\n")

    active_children = []

    try:
        while True:
            # Принимаем новое подключение
            client_sock, client_addr = server.accept()
            print(f"\n[Главный PID {os.getpid()}] Новое подключение от {client_addr}")

            # Создаём новый процесс для обслуживания клиента
            p = Process(
                target=handle_client,
                args=(client_sock, client_addr)
            )
            p.start()
            active_children.append(p)

            # В главном процессе закрываем копию клиентского сокета
            client_sock.close()

            # Очищаем список от завершённых процессов
            active_children = [p for p in active_children if p.is_alive()]

            print(f"[Главный PID {os.getpid()}] Активных процессов-обработчиков: {len(active_children)}")

    except KeyboardInterrupt:
        print(f"\n[Главный PID {os.getpid()}] Получен сигнал остановки сервера")
    finally:
        print(f"[Главный PID {os.getpid()}] Завершаем работу...")
        # Ждём завершения всех дочерних процессов
        for p in active_children:
            if p.is_alive():
                print(f"Ожидание завершения процесса {p.pid}...")
                p.join(timeout=1)
        server.close()
        print("Сервер остановлен")

if __name__ == '__main__':
    start_server()
