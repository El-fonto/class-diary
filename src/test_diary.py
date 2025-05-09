import unittest
from datetime import date, datetime
from diary import Student, Session


class TestStudentClass(unittest.TestCase):
    def test_student_creation(self):
        s1 = Student("Alice", 1)
        s2 = Student("alice", 2)

        self.assertNotEqual(s1, s2)
