# metaclass_project/meta.py
class AutoMethodsMeta(type):
    def __new__(cls, name, bases, dct):
        new_dct = {}
        for attr, value in dct.items():
            if not attr.startswith('__'):
                # Define getter method
                def getter(self, attr=attr):
                    return self.__dict__.get(attr, None)

                # Define setter method with validation for age
                def setter(self, value, attr=attr):
                    if attr == "age" and (not isinstance(value, int) or value <= 0):
                        raise ValueError(f"{attr} must be a positive integer.")
                    self.__dict__[attr] = value

                # Assign the getter and setter as properties
                new_dct[f"get_{attr}"] = getter
                new_dct[f"set_{attr}"] = setter

                # Define property methods
                new_dct[attr] = property(getter, setter)

        # Update the class with the original and generated methods
        new_dct.update(dct)
        return super(AutoMethodsMeta, cls).__new__(cls, name, bases, new_dct)
