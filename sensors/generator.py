import asyncio
import random
import logging
import server
from server import RightechWSClient

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем обработчик для вывода в консоль
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

SENSOR_POS = {
    "sensor-1": {'x': 20, 'y': 35},
    "sensor-2": {'x': 35, 'y': 35},
    "sensor-3": {'x': 20, 'y': 68},
    "sensor-4": {'x': 35, 'y': 68},
    "sensor-5": {'x': 64, 'y': 24},
    "sensor-6": {'x': 64, 'y': 46},
    "sensor-7": {'x': 81, 'y': 24},
    "sensor-8": {'x': 81, 'y': 46},
    "sensor-9": {'x': 64, 'y': 69},
    "sensor-10": {'x': 81, 'y': 69},
}


class DataGenerator:
    def __init__(self, initial_temp=22, initial_hum=50):
        self.temp = initial_temp
        self.hum = initial_hum

    async def next_data(self):
        self.temp = round(self.temp + random.uniform(-0.3, 1.3), 2)
        self.hum = round(self.hum + random.uniform(-0.3, 1.3), 2)
        logger.debug(f"Generated new data: temp={self.temp}, hum={self.hum}")
        return self.temp, self.hum


async def generate_data(object_name: str):
    generator = DataGenerator()
    client = RightechWSClient(object_name)

    try:
        logger.info(f"Starting data generation for {object_name}")
        while True:
            temp, hum = await generator.next_data()
            await client.send({
                "temperature": temp,
                "humidity": hum,
                "locate_x": SENSOR_POS[object_name]['x'],
                "locate_y": SENSOR_POS[object_name]['y']
            })
            await asyncio.sleep(10)
    except Exception as e:
        logger.error(f"Error in {object_name}: {str(e)}", exc_info=True)
    finally:
        await client.close()
        logger.info(f"Closed connection for {object_name}")


async def main():
    try:
        logger.info("Starting main application")
        objects_name_list = await server.get_name_objects()
        logger.info(f"Found objects: {objects_name_list}")

        tasks = [generate_data(name) for name in objects_name_list]
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Application shutdown")


if __name__ == "__main__":
    asyncio.run(main())
