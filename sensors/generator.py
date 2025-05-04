import asyncio
import random
from sensors import server
from sensors.server import RightechWSClient


SENSOR_POS = {
    "sensor-1": {'x': 28, 'y': 10},
    "sensor-2": {'x': 42, 'y': 45}
}


class DataGenerator:
    def __init__(self, initial_temp=22, initial_hum=50):
        self.temp = initial_temp
        self.hum = initial_hum

    async def next_data(self):
        self.temp = round(self.temp + random.uniform(-0.3, 1.5), 2)
        self.hum = round(self.hum + random.uniform(-0.3, 1.5), 2)
        return self.temp, self.hum


async def generate_data(object_name: str):
    generator = DataGenerator()
    client = RightechWSClient(object_name)

    try:
        while True:
            temp, hum = await generator.next_data()
            await client.send({"temperature": temp, "humidity": hum,
                               "locate_x": SENSOR_POS[object_name]['x'],
                               "locate_y": SENSOR_POS[object_name]['y']})
            await asyncio.sleep(10)
    except Exception as e:
        print(f"Error in {object_name}: {e}")
    finally:
        await client.close()


async def main():
    objects_name_list = await server.get_name_objects()

    tasks = [generate_data(name) for name in objects_name_list]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
