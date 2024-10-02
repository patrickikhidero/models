# metaclass_project/person.py
from .meta import AutoMethodsMeta

class Person(metaclass=AutoMethodsMeta):
    name = None
    age = None

    def __init__(self, name, age):
        self.set_name(name)
        self.set_age(age)
