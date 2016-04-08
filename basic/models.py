from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
	name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.name

class Student(models.Model):
	user = models.OneToOneField(User)
	student_id = models.CharField(max_length=100)
	department = models.ForeignKey(Department)

	mobile_number = models.CharField(max_length=10)
	parents_mobile_number = models.CharField(max_length=10)
	parents_email = models.CharField(max_length=100)
	
	def __unicode__(self):
		return str(self.user)

class Designation(models.Model):
	name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class Report(models.Model):
	name = models.CharField(max_length=100)
	query = models.TextField()

	def __unicode__(self):
		return self.name

class Faculty(models.Model):
	user = models.OneToOneField(User)
	faculty_id = models.CharField(max_length=100)
	department = models.ForeignKey(Department)
	designation = models.ForeignKey(Designation)

	def __unicode__(self):
		return str(self.user)

class Course(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=50)
	department = models.ForeignKey(Department)

	def __unicode__(self):
		return self.code + " " + self.code

class Time(models.Model):
	day = models.CharField(max_length=10)
	hour = models.CharField(max_length=10)
	def __unicode__(self):
		return self.day + " " + hour

class Semester(models.Model):
	name = models.CharField(max_length=10)

	def __unicode__(self):
		return self.name

class Room(models.Model):
	number = models.IntegerField()

	def __unicode__(self):
		return self.number

class CourseClass(models.Model):
	room = models.ForeignKey(Room)
	semester = models.ForeignKey(Semester)
	faculty = models.ForeignKey(Faculty)
	time = models.ForeignKey(Time)


class Attendance(models.Model):

	course_class = models.ForeignKey(CourseClass)
	student = models.ForeignKey(Student)

class MarkingUnit(models.Model):

	number = models.CharField(max_length=100)
	room = models.ForeignKey(Room,blank=True)

	def __unicode__(self):
		return self.number