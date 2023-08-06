import aiohttp
import asyncio
from typing import Optional


class Flashlight:
    # Словари цветов и команд вынесены в атрибуты класса для облегчения поддержки и расширения
    COLORS = {1: 'белый', 2: 'красный', 3: 'зеленый', 4: 'синий', 5: 'желтый'}
    COMMANDS = {
        'on': 'turn_on',
        'off': 'turn_off',
        'color': 'change_color',
    }

    def __init__(self, status: int = 0, color: int = 1) -> None:
        # проверка статуса фонаря на целочисленность
        if not isinstance(status, int):
            raise TypeError("Статус должен быть целым числом")
        self.status = status
        self.color = self.COLORS[color]

    # Строковое представление объекта класса
    def __str__(self):
        return f'Фонарь {"включен" if self.status else "выключен"}. Установлен цвет: {self.color}.'

    # Асинхронный метод выполнения полученных команд.
    async def run_command(self, command: str, metadata: Optional[int] = None) -> None:
        # В зависимости от переданной команды, изменяем состояние фонаря и выводим сообщение на экран.
        if command not in self.COMMANDS:
            # По ТЗ неизвестные команды надо просто игнорировать, но при желании можно добавить тут их обработку
            pass
        method_name = self.COMMANDS[command]
        method = getattr(self, method_name)
        method(metadata)

    def turn_on(self):
        if not self.status:
            self.status = 1
            print('Фонарь включен.')
        else:
            raise ValueError('Фонарь уже был включен ранее.')

    def turn_off(self):
        if self.status:
            self.status = 0
            print('Фонарь выключен.')
        else:
            raise ValueError('Фонарь уже был выключен ранее.')

    def change_color(self, metadata):
        if metadata is None or metadata not in self.COLORS:
            raise ValueError('Проблемы с атрибутом цвета фонаря')
        elif self.COLORS[metadata] == self.color:
            print(f'{self.color.capitalize()} цвет уже был установлен ранее.')
        else:
            self.color = self.COLORS[metadata]
            print(f'Установлен {self.color} цвет фонаря.')


# Асинхронная функция обработки сообщений от сервера
async def handle_message(message: dict, flashlight: Flashlight) -> None:
    try:
        # Извлекаем команду и метаданные из сообщения
        command = message['command']
        metadata = message.get('metadata')
        # Выполняем команду на фонаре
        await flashlight.run_command(command, metadata)
    except ValueError as e:
        print(e)


# Асинхронная функция для запуска приложения
async def main():
    # Бесконечный цикл для запроса данных у пользователя.
    while True:
        # Запрос хоста и порта у пользователя. При пустом вводе применяются значения по умолчанию.
        host = input('Введите хост (по умолчанию 127.0.0.1): ') or '127.0.0.1'
        try:
            port = int(input('Введите порт (по умолчанию 9999): ') or 9999)
            if not (0 <= port <= 65535):
                raise ValueError('Некорректный порт')
            # Если порт введен корректно, то выходим из цикла.
            break
        except ValueError as e:
            print(f'Ошибка: {e}')

    try:
        # Создание объекта сессии для взаимодействия с веб-сокетом.
        async with aiohttp.ClientSession() as session:
            # Подключение к веб-сокету на указанный хост и порт.
            async with session.ws_connect(f'http://{host}:{port}') as ws:
                flashlight = Flashlight()
                # Цикл для чтения сообщений от веб-сокета.
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        message = msg.json()
                        await handle_message(message, flashlight)
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print(f'Подключение к веб-сокету завершилось ошибкой: {ws.exception()}')
                        break
    except Exception as e:
        print(f'Ошибка при подключении к веб-сокету: {e}')


if __name__ == '__main__':
    asyncio.run(main())
