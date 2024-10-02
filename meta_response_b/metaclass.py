from types import MethodType

class AutoMethodMeta(type):
    def __new__(cls, name, bases, attrs):
        # Collect all attributes that need methods generated
        for attr_name in attrs.get('__auto_methods__', []):
            # Generate getter
            def getter(self, attr=attr_name):
                return getattr(self, f"_{attr}", None)
            
            # Generate setter with validation
            def setter(self, value, attr=attr_name):
                validator = attrs.get(f"validate_{attr}")
                if validator and not validator(value):
                    raise ValueError(f"Invalid value for {attr}")
                setattr(self, f"_{attr}", value)
            
            # Attach methods to the class
            attrs[f'get_{attr_name}'] = getter
            attrs[f'set_{attr_name}'] = setter
            
            # Create property for direct attribute access with validation
            attrs[attr_name] = property(getter, setter)
        
        return super(AutoMethodMeta, cls).__new__(cls, name, bases, attrs)
