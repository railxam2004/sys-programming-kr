import socket
import asyncio
import time


def test_threaded_client():
    #Тестирование многопоточного сервера
    start_time = time.time()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8889))
    client.send(b"./test_files")  # отправляем путь к тестовой директории

    response = client.recv(4096)
    client.close()

    elapsed = time.time() - start_time
    return elapsed


async def test_async_client():
    #Тестирование асинхронного сервера
    start_time = time.time()

    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(b"./test_files")  # отправляем путь к тестовой директории
    await writer.drain()

    response = await reader.read(4096)
    writer.close()

    elapsed = time.time() - start_time
    return elapsed


def create_test_files():
    #Создает 5 простых тестовых файлов
    import os
    os.makedirs("./test_files", exist_ok=True)

    for i in range(5):
        with open(f"./test_files/file_{i}.txt", "w") as f:
            # Каждый файл содержит i+1 строк
            for j in range(i + 1):
                f.write(f"This is line {j + 1} in file {i}\n")


async def main():
    # Создаем тестовые файлы
    create_test_files()

    print("Запускаю тестирование...")
    print("-" * 40)

    # Тестируем многопоточный сервер
    print("Подключаюсь к многопоточному серверу...")
    threaded_time = test_threaded_client()
    print(f"Многопоточный сервер: {threaded_time:.4f} секунд")

    # Тестируем асинхронный сервер
    print("\nПодключаюсь к асинхронному серверу...")
    async_time = await test_async_client()
    print(f"Асинхронный сервер: {async_time:.4f} секунд")

    print("\n" + "=" * 40)
    print("РЕЗУЛЬТАТЫ СРАВНЕНИЯ:")

    if threaded_time < async_time:
        print(f"Многопоточный сервер быстрее на {async_time - threaded_time:.4f} секунд")
    else:
        print(f"Асинхронный сервер быстрее на {threaded_time - async_time:.4f} секунд")


if __name__ == "__main__":
    asyncio.run(main())