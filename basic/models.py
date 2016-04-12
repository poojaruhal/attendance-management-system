from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class BaseModel(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Department(BaseModel):
	name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.name

class Designation(BaseModel):
	name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class Report(BaseModel):
	name = models.CharField(max_length=100)
	query = models.TextField()

	def __unicode__(self):
		return self.name

class Faculty(BaseModel):
	user = models.OneToOneField(User)
	faculty_id = models.CharField(max_length=100)
	department = models.ForeignKey(Department)
	designation = models.ForeignKey(Designation)

	def __unicode__(self):
		return str(self.user)

class Course(BaseModel):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=50)
	department = models.ForeignKey(Department)

	def __unicode__(self):
		return self.code + " " + self.name

class Time(BaseModel):
	day = models.CharField(max_length=10)
	hour = models.CharField(max_length=10)
	def __unicode__(self):
		return self.day + " " + self.hour

class Semester(BaseModel):
	name = models.CharField(max_length=10)
	start_time =models.CharField(max_length=20,default='2009-01-05 22:14:39')
	end_time  =models.CharField(max_length=20,default='2009-01-05 22:14:39')

	def __unicode__(self):
		return self.name

class Room(BaseModel):
	number = models.IntegerField()

	def __unicode__(self):
		return str(self.number)

class CourseClass(BaseModel):
	room = models.ForeignKey(Room)
	semester = models.ForeignKey(Semester)
	faculty = models.ForeignKey(Faculty)
	time = models.ForeignKey(Time)
	course = models.ForeignKey(Course,blank=True,default=1)

	def __unicode__(self):
		return self.course.name + " | " + self.semester.name + " Semester"

class Student(BaseModel):
	user = models.OneToOneField(User)
	student_id = models.CharField(max_length=100)
	rf_id = models.CharField(max_length=100)
	department = models.ForeignKey(Department)
	course_class = models.ManyToManyField(CourseClass)
	mobile_number = models.CharField(max_length=10)
	parents_mobile_number = models.CharField(max_length=10)
	parents_email = models.CharField(max_length=100)

	def __unicode__(self):
		return str(self.user)

class Attendance(BaseModel):
	course_class = models.ForeignKey(CourseClass)
	student = models.ForeignKey(Student)

class MarkingUnit(BaseModel):

	number = models.CharField(max_length=100)
	room = models.ForeignKey(Room,blank=True)

	def __unicode__(self):
		return self.number