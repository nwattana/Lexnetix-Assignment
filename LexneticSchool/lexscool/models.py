from django.db import models
from datetime import datetime


class schools(models.Model):
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    email=models.CharField(max_length=100, blank=True)
    tel=models.CharField(max_length=100, blank=True)

class headmasters(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True)
    tel = models.CharField(max_length=100, null=True)
    school = models.OneToOneField('schools', on_delete=models.SET_NULL, null=True)


class teachers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True)
    tel = models.CharField(max_length=100, null=True)
    school = models.ForeignKey('schools', on_delete=models.SET_NULL, null=True)



class students(models.Model):
    YEAR_IN_SCHOOL = [
        ('1','First Year'),
        ('2','Secound Year'),
        ('3','Third Year'),
        ('4','Final Year maybe'),
        ('5','Why you here')
    ]
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=1,choices=YEAR_IN_SCHOOL, default='1')
    school = models.ForeignKey('schools', on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey('teachers', on_delete=models.SET_NULL, null=True)


class tclasses(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)
    student = models.ManyToManyField(students)
    teacher = models.ForeignKey(teachers, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(schools, on_delete=models.CASCADE, null=True)

