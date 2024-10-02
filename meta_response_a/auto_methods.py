from types import MethodType

class AutoMethodsMeta(type):
    def __new__(cls, name, bases, attrs):
        # Collect attributes for which we want to generate methods
        for attr_name in attrs.get('__auto_attributes__', []):
            if attr_name not in attrs:
                continue
            
            # Getter
            def getter(self, attr=attr_name):
                return getattr(self, f"_{attr}", None)
            
            # Setter with validation
            def setter(self, value, attr=attr_name):
                validator = attrs.get(f"validate_{attr}")
                if validator and not validator(value):
                    raise ValueError(f"Invalid value for {attr}: {value}")
                setattr(self, f"_{attr}", value)
            
            # Create property
            attrs[f"get_{attr_name}"] = property(getter)
            attrs[f"set_{attr_name}"] = MethodType(setter, None, attrs[f"get_{attr_name}"])
            
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def validate_positive_integer(value):
        """Validate if the value is a positive integer."""
        return isinstance(value, int) and value > 0

    @staticmethod
    def validate_string(value):
        """Validate if the value is a non-empty string."""
        return isinstance(value, str) and len(value.strip()) > 0