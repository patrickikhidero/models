import unittest
from model import Person

class TestAutoMethods(unittest.TestCase):
    
    def setUp(self):
        self.person = Person("Alice", 30)

    def test_getters(self):
        self.assertEqual(self.person.get_name(), "Alice")
        self.assertEqual(self.person.get_age(), 30)

    def test_setters(self):
        self.person.set_name("Bob")
        self.person.set_age(25)
        self.assertEqual(self.person.get_name(), "Bob")
        self.assertEqual(self.person.get_age(), 25)

    def test_validation_age(self):
        with self.assertRaises(ValueError):
            self.person.set_age(-5)
        with self.assertRaises(ValueError):
            self.person.set_age("not an int")

    def test_validation_name(self):
        with self.assertRaises(ValueError):
            self.person.set_name("")
        with self.assertRaises(ValueError):
            self.person.set_name(123)

    def test_init_validation(self):
        with self.assertRaises(ValueError):
            Person("   ", 20)  # Whitespace name
        with self.assertRaises(ValueError):
            Person("Valid", -1)

if __name__ == '__main__':
    unittest.main()