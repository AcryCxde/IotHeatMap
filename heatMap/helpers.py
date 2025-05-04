import aiohttp
import numpy as np
from config import *
from sensors.server import get_name_objects


class TemperatureMap:
    def __init__(self, grid_size=100, base_temp=20.0, heat_radius=15):
        self.grid_size = grid_size
        self.base_temp = base_temp
        self.heat_radius = heat_radius
        self.map = np.full((grid_size, grid_size), base_temp)

    def reset(self):
        self.map.fill(self.base_temp)

    def apply_heat_source(self, x, y, temp):
        delta = temp - self.base_temp
        for dy in range(-self.heat_radius, self.heat_radius + 1):
            for dx in range(-self.heat_radius, self.heat_radius + 1):
                xi, yi = x + dx, y + dy
                if 0 <= xi < self.grid_size and 0 <= yi < self.grid_size:
                    distance = np.sqrt(dx ** 2 + dy ** 2)
                    if distance <= self.heat_radius:
                        falloff = 1 - (distance / self.heat_radius)
                        self.map[yi, xi] += delta * falloff

    async def update_from_rightech(self):
        self.reset()
        objects_name = await get_name_objects()
        async with aiohttp.ClientSession() as session:
            for object_name in objects_name:
                url = f"{HOST}/api/v1/objects/{object_name}"
                headers = {
                    'authorization': f'Bearer {AUTH_TOKEN}',
                    'content-type': 'application/json'
                }
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        x = int(data['state']['locate_x'])
                        y = int(data['state']['locate_y'])
                        temp = float(data['state']['temperature'])
                        self.apply_heat_source(x, y, temp)
