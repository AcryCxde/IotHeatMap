import json
import aiohttp
import websockets

from config import AUTH_TOKEN, WS_HOST, HOST


class RightechWSClient:
    def __init__(self, object_id="sensor-1"):
        self.websocket = None
        self.uri = f"{WS_HOST}/objects/{object_id}/connect"

    async def connect(self):
        """Подключиться к серверу"""
        self.websocket = await websockets.connect(self.uri)
        print(f"Connected to {self.uri}")

    async def send(self, data: dict):
        """Отправить данные (автоматически подключается если нет соединения)"""
        if not self.websocket:
            await self.connect()
        data = json.dumps(data)
        await self.websocket.send(data)
        print(f"Sent: {data}")

    async def close(self):
        """Закрыть соединение"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            print("Connection closed")


async def get_name_objects():
    """Асинхронный HTTP-запрос для получения объектов"""
    url = f"{HOST}/api/v1/objects"
    headers = {
        'authorization': f'Bearer {AUTH_TOKEN}',
        'content-type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                names = []
                response = await response.json()
                for object_data in response:
                    try:
                        names.append(object_data['name'])
                    except Exception as e:
                        raise Exception(f"No object names. Error: {e}")
                return names
            else:
                raise Exception(f"HTTP error: {response.status}")
