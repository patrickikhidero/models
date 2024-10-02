# tests/test_person.py
import unittest
from metaclass_project.person import Person

class TestPerson(unittest.TestCase):

    def test_get_set_name(self):
        person = Person("Alice", 25)
        self.assertEqual(person.get_name(), "Alice")
        person.set_name("Bob")
        self.assertEqual(person.get_name(), "Bob")
        self.assertEqual(person.name, "Bob")  # property method check

    def test_get_set_age(self):
        person = Person("Alice", 25)
        self.assertEqual(person.get_age(), 25)
        person.set_age(30)
        self.assertEqual(person.get_age(), 30)
        self.assertEqual(person.age, 30)  # property method check

    def test_invalid_age(self):
        with self.assertRaises(ValueError):
            Person("Alice", -5)  # Age should be positive
        
        person = Person("Alice", 25)
        with self.assertRaises(ValueError):
            person.set_age(-10)  # Age should be positive

if __name__ == "__main__":
    unittest.main()
