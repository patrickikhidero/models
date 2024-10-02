import unittest
from base_class import Person

class TestAutoMethodMeta(unittest.TestCase):

    def setUp(self):
        self.person = Person()

    def test_get_set_name(self):
        self.person.set_name("Alice")
        self.assertEqual(self.person.get_name(), "Alice")
        self.assertEqual(self.person.name, "Alice")

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            self.person.set_name("")  # Empty name should raise ValueError

    def test_get_set_age(self):
        self.person.set_age(30)
        self.assertEqual(self.person.get_age(), 30)
        self.assertEqual(self.person.age, 30)

    def test_invalid_age(self):
        with self.assertRaises(ValueError):
            self.person.set_age(-5)  # Negative age should raise ValueError
        with self.assertRaises(ValueError):
            self.person.set_age("30")  # String should also raise ValueError

    def test_property_access(self):
        # Test if setting through property works with validation
        self.person.name = "Bob"
        self.person.age = 25
        self.assertEqual(self.person.name, "Bob")
        self.assertEqual(self.person.age, 25)

    def test_direct_attribute_access(self):
        # This might not be encouraged but should still work with the property setup
        with self.assertRaises(AttributeError):  # since we're using properties, direct access should fail
            self.person._name = "Direct"

if __name__ == '__main__':
    unittest.main()