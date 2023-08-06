import unittest
from unittest.mock import patch, AsyncMock

from .flashlight import Flashlight, main, handle_message


class TestFlashlight(unittest.TestCase):
    def setUp(self):
        self.flashlight = Flashlight()

    # тесты конструктора класса Flashlight
    def test_init_with_defaults(self):
        self.assertEqual(self.flashlight.status, 0)
        self.assertEqual(self.flashlight.color, 'белый')

    def test_init_with_status_and_color(self):
        f = Flashlight(status=1, color=3)
        self.assertEqual(f.status, 1)
        self.assertEqual(f.color, 'зеленый')

    def test_init_with_invalid_color(self):
        with self.assertRaises(KeyError):
            Flashlight(color=6)

    def test_init_with_invalid_status(self):
        with self.assertRaises(TypeError):
            Flashlight(status='on')

    # тесты строкового представления
    def test_str(self):
        self.assertEqual(str(self.flashlight), 'Фонарь выключен. Установлен цвет: белый.')

    # тесты функции run_command
    async def test_run_command(self):
        # тесты включения
        await self.flashlight.run_command('on')
        self.assertEqual(self.flashlight.status, 1)
        self.assertEqual(self.flashlight.color, 'белый')
        self.assertRaises(ValueError, self.flashlight.run_command, 'on')

        # тесты выключения
        await self.flashlight.run_command('off')
        self.assertEqual(self.flashlight.status, 0)
        self.assertEqual(self.flashlight.color, 'белый')
        self.assertRaises(ValueError, self.flashlight.run_command, 'off')

        # тесты установки цвета
        await self.flashlight.run_command('color', 2)
        self.assertEqual(self.flashlight.status, 0)
        self.assertEqual(self.flashlight.color, 'красный')
        self.assertRaises(ValueError, self.flashlight.run_command, 'color', 6)

        async with self.assertRaises(ValueError):
            await self.flashlight.run_command('color', 6)


class TestHandleMessage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.flashlight = AsyncMock()

    async def test_handle_message_on(self):
        await handle_message({'command': 'on'}, self.flashlight)
        self.flashlight.run_command.assert_called_once_with('on', None)

    async def test_handle_message_off(self):
        await handle_message({'command': 'off'}, self.flashlight)
        self.flashlight.run_command.assert_called_once_with('off', None)

    async def test_handle_message_color(self):
        await handle_message({'command': 'color', 'metadata': 2}, self.flashlight)
        self.flashlight.run_command.assert_called_once_with('color', 2)


class TestMain(unittest.IsolatedAsyncioTestCase):

    @patch('builtins.input', side_effect=['127.0.0.1', '9999'])
    @patch('aiohttp.ClientSession.ws_connect')
    @patch('flashlight.handle_message')
    async def test_main(self, handle_mock, ws_connect_mock, input_mock):
        # Устанавливаем mock-объекты
        ws_mock = AsyncMock()
        msg_mock = AsyncMock()
        ws_mock.__aiter__.return_value = [msg_mock]

        # Задаем поведение мок-объектов
        ws_connect_mock.return_value.__aenter__.return_value = ws_mock
        msg_mock.type = 'text'
        msg_mock.json.return_value = {'message': 'test'}

        # Вызываем тестируемую функцию
        await main()

        # Проверяем, что вызовы были выполнены с корректными аргументами
        ws_connect_mock.assert_called_once_with('http://127.0.0.1:9999')


if __name__ == '__main__':
    unittest.main()
