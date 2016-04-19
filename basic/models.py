from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import time
import utils
# from utils import CheckEvenOdd
# from utils import SemesterNumber
# from utils import GetDayName 
# from utils import 

# Create your models here.

class BaseModel(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

class Department(BaseModel):
	name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=20)

	def __str__(self):
		return self.name

class Course(BaseModel):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=50)
	department = models.ForeignKey(Department)

	def __str__(self):
		return self.code + " " + self.name


class Designation(BaseModel):
	name = models.CharField(max_length=100)
	acronym = models.CharField(max_length=20)
	def __str__(self):
		return self.name

class Report(BaseModel):
	name = models.CharField(max_length=100)
	query = models.TextField()

	def __str__(self):
		return self.name

class Faculty(BaseModel):
	user = models.OneToOneField(User)
	faculty_id = models.CharField(max_length=100)
	department = models.ForeignKey(Department)
	designation = models.ForeignKey(Designation)

	def __str__(self):
		return str(self.user)

class Time(BaseModel):
	day = models.CharField(max_length=10)
	hour = models.CharField(max_length=10)
	def __str__(self):
		return self.day + " " + self.hour

class Semester(BaseModel):
	name = models.CharField(max_length=10)
	year = models.CharField(max_length=4)
	#start_time =models.DateTimeField(auto_now_add=True)
	start_time = models.DateTimeField(default=datetime.now, blank=True)
	end_time = models.DateTimeField(default=datetime.now, blank=True)
	#end_time  =models.CharField(max_length=20,default='2009-01-05 22:14:39')

	@staticmethod
	def getCurrentSemesterNumber():

		localtime = time.localtime(time.time())
		yr = localtime.tm_year
		month = localtime.tm_mon
		semesterNumber = utils.CheckEvenOdd(month)
		
		# Get Semester
		if semesterNumber == utils.SemesterNumber.odd:
			semesterNumber = "odd"
		elif semesterNumber == utils.SemesterNumber.even:
			semesterNumber = "even"

		semester = Semester.objects.filter(name=semesterNumber , year=yr).get()

		return semester

	def __str__(self):
		return self.name + self.year

class Room(BaseModel):
	number = models.IntegerField()

	def __str__(self):
		return str(self.number)

class CourseClass(BaseModel):
	room = models.ForeignKey(Room)
	semester = models.ForeignKey(Semester)
	faculty = models.ForeignKey(Faculty)
	time = models.ForeignKey(Time)
	course = models.ForeignKey(Course,blank=True,default=1)

	def __str__(self):
		return self.course.name + " | " + self.semester.name + " Semester"


class Student(BaseModel):
	user = models.OneToOneField(User)
	student_id = models.CharField(max_length=100)
	rf_id = models.CharField(max_length=100)
	department = models.ForeignKey(Department)
	courseClass = models.ManyToManyField(CourseClass)
	mobile_number = models.CharField(max_length=10)
	parents_mobile_number = models.CharField(max_length=10)
	parents_email = models.CharField(max_length=100)

	def __str__(self):
		return str(self.user)

	@staticmethod
	def mark_attendance(rfid,deviceId):

		if rfid:
			#time.struct_time(tm_year=2016, tm_mon=4, tm_mday=11, tm_hour=9, tm_min=20, tm_sec=21, tm_wday=0, tm_yday=102, tm_isdst=1)

			#st1 = Student.objects.filter(rf_id=rfid)
			#student1 = st1[0]

			st = Student.objects.get(rf_id=rfid)
			#student=st[0]

			localtime = time.localtime(time.time())
			yr=localtime.tm_year
			month=localtime.tm_mon
			hr=localtime.tm_hour
			print(hr)
			semesterNumber=utils.CheckEvenOdd(month)		
			# Get Semester
			if semesterNumber == utils.SemesterNumber.odd:
				semesterNumber = "odd"
			elif semesterNumber == utils.SemesterNumber.even:
				semesterNumber = "even"

			semester_d = Semester.objects.get(name=semesterNumber , year=yr)
			time_d = Time.objects.filter(day= utils.GetDayName(localtime.tm_wday), hour = hr)

			if time_d:
				time_d = time_d.get()
			else:
				return "No class"


			# Get time

			# Get room from device id posted
			room_d=MarkingUnit.objects.get(number=deviceId).room
			#room_d=Room.objects.get(number=room_marking_d.)
			course_class_d=CourseClass.objects.filter(semester=semester_d.pk,time=time_d.pk,room=room_d).get();

			courseAssinged=0
			for cs in st.courseClass.all():
				if(cs==course_class_d):
					courseAssinged=1

			if(course_class_d and courseAssinged):
				attendance = Attendance(course_class=course_class_d, student=st)
				attendance.save()
				html = """student {0} & course {1}""".format(st.user.username, course_class_d.course.name)
			else:
				html = """Not regiestered"""

			#course = Course.objects.filter(name="VLSI Design").get()

			#courseclass = CourseClass.objects.filter(course=course.pk,semester=semester.pk).get()

		else:

			html = "No id passed"

		return html


class Attendance(BaseModel):
	course_class = models.ForeignKey(CourseClass)
	student = models.ForeignKey(Student)

	@staticmethod
	def getStudentsWithLessAttendance():
		StudentsCourseListToSendMesg=[]
		students = Student.objects.all()

		currentSemester = Semester.getCurrentSemesterNumber()

		attendance_threshold = utils.CalculateThreshold(currentSemester)

		for student in students:
			attendences = Attendance.objects.filter(student=student.pk)
			for course_class in student.courseClass.all():
				course_att_count = utils.CourseAttendanceCount()
				course_att_count.student_id=student.student_id
				course_att_count.course_name = course_class.course.name
				for att in attendences:
					if (att.course_class == course_class):
						course_att_count.attendance_count += 1
				if (course_att_count.attendance_count < attendance_threshold):
					course_att_count.student_parentno = student.parents_mobile_number
					course_att_count.student_email = student.parents_email
					course_att_count.student_name = student.user.username

					element = {
						"student_name": str(course_att_count.student_name),
						"student_id":str(course_att_count.student_id),
						"course_name":str(course_att_count.course_name),
						"attendance_count":str(course_att_count.attendance_count),
						"student_parentno":str(course_att_count.student_parentno),
						"student_email":str(course_att_count.student_email)
					}

					#StudentsCourseListToSendMesg.append(course_att_count)
					StudentsCourseListToSendMesg.append(element)

		return StudentsCourseListToSendMesg

class MarkingUnit(BaseModel):

	number = models.CharField(max_length=100)
	room = models.ForeignKey(Room,blank=True)

	def __str__(self):
		return self.number

