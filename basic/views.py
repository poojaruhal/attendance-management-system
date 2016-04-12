from django.shortcuts import render
import datetime
from django.http import HttpResponse,JsonResponse
import time
import json
from .models import Faculty
from enum import Enum
from .models import Student,Semester,Attendance,Course,CourseClass,MarkingUnit,Time,Room

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):

	return render(request,'basic/welcome.html')
@login_required(login_url='/login/')
def student(request):

	student = Student.objects.filter(user=request.user)

	if not student:
		# Logged in user is not a student
		return render(request,'basic/permission_error.html')

	student = student.get()

	return render(request,'basic/student_course_wise_attendance.html')

@login_required(login_url='/login/')
def faculty(request):

	# Allowed only for faculties

	faculty = Faculty.objects.filter(user=request.user)
	
	if not faculty:
		# Logged in user is not a faculty
		return render(request,'basic/permission_error.html')

	faculty = faculty.get()

	# Courses taught by current logged in user

	courses = CourseClass.objects.filter(faculty=faculty)

	if not courses:
		# Current faculty doesn't teach any course
		return render(request,'basic/no_course.html')	

	# X- Axis
	categories = []

	for i in range(1,11):
		categories.append('Week '+str(i))

	# Series Data
	
	attendance = {}
	attendance['ses'] = [1,2,3,4,5,6,7,8,9,10,11]
	attendance['vlsi'] = [11,10,9,8,7,6,5,4,3,2,1]

	series = []

	series.append({'name':'SES','data':attendance['ses']})
	series.append({'name':'VLSI Design','data':attendance['vlsi']})

	context = {'categories':categories,'series':series}

	return render(request,'basic/course_list.html',context=context)

# Create your views here.

class CourseAttendanceCount:
	course_name = ""
	attendance_count = 0
	student_id = ""
	student_parentno=""
	student_email=""

	def to_dict(self):
		return {"student_id":str(self.student_id), "course_name":str(self.course_name),"attendance_count":str(self.attendance_count) }

	def _str_(self):
		return self.student_id + " " + self.course_name + " " + self.attendance_count


class SemesterNumber(Enum):
	even = 1
	odd = 2

	def index(request):
		return render(request, 'basic/index.html')


@csrf_exempt

def mark_attendance(request):

	#rfid = request.POST.get("rfid","")
	rfid="226545398"
	deviceID="5"
	#time = request.POST.get("time", "")
	#deviecID = request.POST.get("deviceID", "")

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
		semesterNumber=CheckEvenOdd(month)
		# Get Semester
		semester_d = Semester.objects.get(name=semesterNumber , year=yr)
		time_d = Time.objects.get(day= GetDayName(localtime.tm_wday), hour = hr)

		# Get time

		# Get room from device id posted
		room_d=MarkingUnit.objects.get(number=deviceID).room
		#room_d=Room.objects.get(number=room_marking_d.)
		course_class_d=CourseClass.objects.filter(semester=semester_d.pk,time=time_d.pk,room=room_d).get();

		courseAssinged=0
		for cs in st.courseClass.all():
			if(cs==course_class_d):
				courseAssinged=1

		if(course_class_d and courseAssinged):
			attendance = Attendance(course_class=course_class_d, student=st)
			attendance.save()
			html = """<html><body>Marked Attendance for student {0} and course {1} .</body></html>""".format(st.user.username, course_class_d.course.name)
		else:
			html = """<html><body>student {0} is not regiestered for course {1} .</body></html>""".format(st.user.username, course_class_d.course.name)

		#course = Course.objects.filter(name="VLSI Design").get()

		#courseclass = CourseClass.objects.filter(course=course.pk,semester=semester.pk).get()





		


	else:

		html = "<html><body>%s.</body></html>" % "No id passed"
	
	return HttpResponse(html)


def CheckEvenOdd(month):

	if(month==1 & month==2 & month==3 & month==4 & month==5 & month==6) :
		return SemesterNumber.even.name
	else :
		return SemesterNumber.odd.name


def GetDayName(dayNo) :
	if(dayNo==0) :
		return "monday"

	if (dayNo == 1):
		return "tuesday"

	if (dayNo == 2):
		return "wednesday"

	if (dayNo == 3):
		return "thursday"

	if (dayNo == 4):
		return "friday"

	if (dayNo == 5):
		return "saturday"

	if (dayNo == 5):
		return "sunday"



def SendMessageForAllStudentInAllCourses(request):
	StudentsCourseListToSendMesg=[]
	students = Student.objects.all()
	attendance_threshold = 1
	for student in students:
		attendences = Attendance.objects.filter(student=student.pk)
		for course_class in student.courseClass.all():
			course_att_count = CourseAttendanceCount()
			course_att_count.student_id=student.student_id
			course_att_count.course_name = course_class.course.name
			for att in attendences:
				if (att.course_class == course_class):
					course_att_count.attendance_count += 1
			if (course_att_count.attendance_count < attendance_threshold):
				course_att_count.student_parentno = student.parents_mobile_number
				course_att_count.student_email = student.parents_email

				element = {
					"student_id":str(course_att_count.student_id),
					"course_name":str(course_att_count.course_name),
					"attendance_count":str(course_att_count.attendance_count),
					"student_parentno":str(course_att_count.student_parentno),
					"student_email":str(course_att_count.student_email)
				}

				#StudentsCourseListToSendMesg.append(course_att_count)
				StudentsCourseListToSendMesg.append(element)

	#html = """<html><body>Marked Attendance for count {0} .</body></html>""".format(len(StudentsCourseListToSendMesg))
	html = StudentsCourseListToSendMesg
	return JsonResponse(html,safe=False)


def SendMessageForStudent(request):
	student_id = request.POST.get("student_id", "")


def SendMessageForCourse(request):
	course_id = request.POST.get("course_name", "")

