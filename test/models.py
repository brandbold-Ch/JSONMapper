from datetime import datetime
from uuid import uuid4
from jsonmapper.types import StringField, UUIDField, DateField, IntegerField
from jsonmapper.mapper.base import Model, JsonStore


class User(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    name = StringField(max_length=13, min_length=10)
    lastname = StringField(max_length=50)
    birthdate = DateField()
    timestamp = DateField(default=datetime.now().date())
    child = IntegerField(7, min_value=0)
    wifes = IntegerField(1, min_value=0)
    role = StringField(default="USER")


class Admin(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    role = StringField(default="ADMIN")
    children = IntegerField("6", min_value=0)


JsonStore(db_name="centinel", db_path="/database/")


user = User(
    name="Brandon Jared",
    lastname="Molina Vazquez",
    birthdate="2004-06-04"
)

print(user.child)
