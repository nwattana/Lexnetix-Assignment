from django.test import TestCase
import unittest
from django.test import Client
from .schemas import *
from .api import *
from .models import *

SCHOOL_IN_1 = SchoolBase(
    name = "school 1",
    email = "school 1",
    address = "school 1",
    tel = "school 1",
)
SCHOOL_IN_2 = SchoolBase(
    name = "school 2",
    email = "school 2",
    address = "school 2",
    tel = "school 2",
)
SCHOOL_IN_3 = SchoolBase(
    name = "school 3",
    email = "school 3",
    address = "school 3",
    tel = "school 3",
)

class BasicGetPost(unittest.TestCase):
    def setUp(self):
        school1 = school_create(None, SCHOOL_IN_1)
        school2 = school_create(None, SCHOOL_IN_2)
        school3 = school_create(None, SCHOOL_IN_3)
        
    def test_get_school_1(self):
        result = (200, schools.objects.get(id=1))
        response = school_get_by_id(None, school_id = 1)
        self.assertEqual(result, response)
        
    def test_get_school_2(self):
        result = (200, schools.objects.get(id=2))
        response = school_get_by_id(None, school_id = 2)
        self.assertEqual(result, response)

    def test_get_school_3(self):
        result = (200, schools.objects.get(id=3))
        response = school_get_by_id(None, school_id = 3)
        self.assertEqual(result, response)
        
class BasicPostSchool(unittest.TestCase):
    def setUp(self):
        school1 = school_create(None, SCHOOL_IN_1)
        school2 = school_create(None, SCHOOL_IN_2)
        
    def test_no_duplicate_School(self):
        before = len(schools.objects.all())
        response = school_create(None, SCHOOL_IN_2)
        after = len(schools.objects.all())
        self.assertEqual(after, before)
        self.assertEqual(response, (200, schools.objects.get(pk=2)))
    
        
class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/api/school')
        self.assertEqual(response.status_code, 200)