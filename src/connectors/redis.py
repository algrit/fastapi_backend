import redis.asyncio as redis

class AsyncRedisClient:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        """
        Инициализация асинхронного клиента Redis.

        :param host: Адрес сервера Redis.
        :param port: Порт сервера Redis.
        :param db: Номер базы данных (по умолчанию 0).
        """
        self.host = host
        self.port = port
        self.db = db
        self.client = None

    async def connect(self):
        """Подключение к Redis."""
        self.client = await redis.create_redis_pool(
            (self.host, self.port), db=self.db
        )

    async def close(self):
        """Закрытие соединения с Redis."""
        if self.client:
            self.client.close()
            await self.client.wait_closed()

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """
        Устанавливает значение для указанного ключа.

        :param key: Ключ.
        :param value: Значение.
        :param ex: Время жизни ключа в секундах (необязательно).
        :return: True, если операция успешна.
        """
        try:
            await self.client.set(key, value, expire=ex)
            return True
        except aioredis.RedisError as e:
            print(f"Ошибка при установке значения: {e}")
            return False

    async def get(self, key: str) -> Optional[str]:
        """
        Получает значение по ключу.

        :param key: Ключ.
        :return: Значение или None, если ключ не существует.
        """
        try:
            value = await self.client.get(key, encoding='utf-8')
            return value
        except aioredis.RedisError as e:
            print(f"Ошибка при получении значения: {e}")
            return None

    async def delete(self, key: str) -> bool:
        """
        Удаляет ключ.

        :param key: Ключ.
        :return: True, если операция успешна.
        """
        try:
            result = await self.client.delete(key)
            return result > 0
        except aioredis.RedisError as e:
            print(f"Ошибка при удалении ключа: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        Проверяет существование ключа.

        :param key: Ключ.
        :return: True, если ключ существует, иначе False.
        """
        try:
            return await self.client.exists(key)
        except aioredis.RedisError as e:
            print(f"Ошибка при проверке существования ключа: {e}")
            return False

    async def keys(self, pattern: str = '*') -> list:
        """
        Получает все ключи, соответствующие шаблону.

        :param pattern: Шаблон для поиска ключей.
        :return: Список ключей.
        """
        try:
            return [key.decode('utf-8') for key in await self.client.keys(pattern)]
        except aioredis.RedisError as e:
            print(f"Ошибка при получении ключей: {e}")
            return []

    async def set_multiple(self, mapping: Dict[str, str], ex: Optional[int] = None) -> bool:
        """
        Устанавливает несколько значений сразу.

        :param mapping: Словарь с ключами и значениями.
        :param ex: Время жизни ключей в секундах (необязательно).
        :return: True, если операция успешна.
        """
        try:
            for key, value in mapping.items():
                await self.client.set(key, value, expire=ex)
            return True
        except aioredis.RedisError as e:
            print(f"Ошибка при установке нескольких значений: {e}")
            return False

    async def get_multiple(self, keys: list) -> dict:
        """
        Получает несколько значений по ключам.

        :param keys: Список ключей.
        :return: Словарь с ключами и значениями.
        """
        try:
            values = await self.client.mget(*keys)
            return dict(zip(keys, [v.decode('utf-8') if v else None for v in values]))
        except aioredis.RedisError as e:
            print(f"Ошибка при получении нескольких значений: {e}")
            return {}

# Пример использования
async def main():
    redis_client = AsyncRedisClient()

    # Подключаемся к Redis
    await redis_client.connect()

    # Устанавливаем значение
    await redis_client.set("name", "Alice")

    # Получаем значение
    print(await redis_client.get("name"))

    # Проверка существования ключа
    print(await redis_client.exists("name"))

    # Удаление ключа
    await redis_client.delete("name")

    # Закрытие соединения
    await redis_client.close()

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
