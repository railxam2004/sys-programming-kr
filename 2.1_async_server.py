import asyncio
import os
from pathlib import Path


async def count_lines_in_file(filepath):
#Асинхронно считает строки в одном файле
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except:
        return 0


async def handle_client(reader, writer):
#Обработка подключения клиента
    data = await reader.read(1024)
    directory = data.decode().strip()

    if not os.path.exists(directory):
        writer.write(b"Directory not found")
        await writer.drain()
        writer.close()
        return

    files = [f for f in Path(directory).iterdir() if f.is_file()]
    results = {}

    #Асинхронно обрабатываем все файлы
    tasks = []
    for file in files:
        task = asyncio.create_task(count_lines_in_file(file))
        tasks.append((file.name, task))

    for filename, task in tasks:
        results[filename] = await task

    # Отправляем результаты
    response = str(results).encode()
    writer.write(response)
    await writer.drain()
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())