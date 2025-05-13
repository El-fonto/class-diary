import unittest
from diary import Student


class TestStudentClass(unittest.TestCase):
    def test_student_creation(self):
        s1 = Student("Alice")
        s2 = Student("Alice")

        self.assertEqual(s1.name, s2.name)
        self.assertNotEqual(s1.id, s2.id)

    def test_json_creation(self):
        pass
