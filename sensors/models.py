from peewee import *

db = SqliteDatabase('../data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Sensor(BaseModel):
    location_x = IntegerField(null=False)
    location_y = IntegerField(null=False)
    temperature = IntegerField(null=False)
    humidity = IntegerField(null=False)
