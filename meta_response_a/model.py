from auto_methods import AutoMethodsMeta

class Person(metaclass=AutoMethodsMeta):
    __auto_attributes__ = ['name', 'age']
    
    def validate_age(value):
        return AutoMethodsMeta.validate_positive_integer(value)
    
    def validate_name(value):
        return AutoMethodsMeta.validate_string(value)

    def __init__(self, name, age):
        self.name = name
        self.age = age  # This will use the generated setter