from datetime import datetime
from uuid import uuid4
from jsonmapper.types import StringField, UUIDField, DateField, FloatField, IntegerField
from jsonmapper.mapper.base import Model, JsonStore


class Pet(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    name = StringField(max_length=30, min_length=2)
    species = StringField(max_length=20, min_length=3)
    birthdate = DateField()
    owner_id = UUIDField()
    timestamp = DateField(default=datetime.now().date())
    status = StringField(default="AVAILABLE")


class Appointment(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    pet_id = UUIDField()
    user_id = UUIDField()
    date = DateField()
    description = StringField(max_length=200, default="No description provided")
    timestamp = DateField(default=datetime.now().date())


class Product(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    name = StringField(max_length=50, min_length=3)
    description = StringField(max_length=300)
    price = FloatField()
    timestamp = DateField(default=datetime.now().date())


class Order(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    user_id = UUIDField()
    product_id = UUIDField()
    quantity = IntegerField(default=1)
    total_price = FloatField()
    timestamp = DateField(default=datetime.now().date())
    status = StringField(default="PENDING")


class Feedback(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    user_id = UUIDField()
    content = StringField(max_length=500)
    timestamp = DateField(default=datetime.now().date())
    rating = IntegerField(min_length=1, max_length=5)


class User(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    name = StringField(max_length=13, min_length=10)
    lastname = StringField(max_length=50)
    birthdate = DateField()
    timestamp = DateField(default=datetime.now().date())
    role = StringField(default="USER")


class Admin(Model):
    id = UUIDField(default=lambda: uuid4(), unique=True)
    role = StringField(default="ADMIN")


JsonStore(db_name="centinel", db_path="/database/")


if __name__ == "__main__":
    user = User()
    user.name = "Brandon Jared"
    user.lastname = "Moliba Vazquez"
    user.birthdate = "2004-06-04"
    user.timestamp = datetime.now().date()
