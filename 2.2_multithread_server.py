import socket
import threading
import os
from pathlib import Path
import time


def count_lines_in_file(filepath):
    #Считает строки в одном файле
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except:
        return 0


def handle_client(client_socket, directory):
    # Обработка клиента в отдельном потоке
    files = [f for f in Path(directory).iterdir() if f.is_file()]
    results = {}

    # Обрабатываем файлы последовательно (можно сделать пул потоков)
    for file in files:
        results[file.name] = count_lines_in_file(file)

    # Отправляем результаты
    response = str(results).encode()
    client_socket.send(response)
    client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8889))
    server.listen(5)

    test_directory = "./test_files"  # Тестовая директория

    print("Многопоточный сервер запущен...")

    while True:
        client_socket, addr = server.accept()
        # Создаем новый поток для каждого клиента
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, test_directory)
        )
        client_thread.start()


if __name__ == "__main__":
    main()