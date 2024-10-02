from metaclass import AutoMethodMeta
from validators import positive_integer

class Person(metaclass=AutoMethodMeta):
    __auto_methods__ = ['name', 'age']

    def validate_name(value):
        return isinstance(value, str) and len(value.strip()) > 0

    def validate_age(value):
        return positive_integer(value)
