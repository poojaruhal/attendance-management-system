from django.shortcuts import render
import datetime
from django.http import HttpResponse,JsonResponse
import time
import math
import json
from .models import Faculty
from enum import Enum
from .models import Student,Semester,Attendance,Course,CourseClass,MarkingUnit,Time,Room

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives

from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from itertools import islice
from chartjs.colors import next_color, COLORS
from django.db.models import Count

class SemesterNumber(Enum):
	even = 1
	odd = 2


def CheckEvenOdd(month):

	if(month==1 & month==2 & month==3 & month==4 & month==5 & month==6) :
		return SemesterNumber.odd
	else :
		return SemesterNumber.even


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

	default_select = "Choose Subject"
	
	subject = request.GET.get("subject",default=default_select) 


	f = Faculty.objects.filter(user=request.user)
	
	if f:
	
		f = f.get()

		course_list = []
		
		courses = CourseClass.objects.filter(faculty=f)

		for c in courses:
			course_list.append(c.course)

		context = {'courses':course_list,'subject':subject}

		# User has selected a course to view report
		if subject != default_select:
			# Generate report for the selected course
			# Report needs :
			#  - current semester
			#  - current faculty
			#  - selected course

			# TODO Move to a function
			localtime = time.localtime(time.time())
			yr=localtime.tm_year
			month=localtime.tm_mon
			hr=localtime.tm_hour			
			semesterNumber=CheckEvenOdd(month)
			
			if semesterNumber == SemesterNumber.odd:
				semesterNumber = "odd"
			elif semesterNumber == SemesterNumber.even:
				semesterNumber = "even"

			# Get Semester
			semester = Semester.objects.filter(name=semesterNumber , year=yr)
			
			# Selected Course
			course = Course.objects.filter(name=subject).get()

			courseclass = CourseClass.objects.filter(semester=semester,course=course,faculty=f)

			#attendances = Attendance.objects.filter(course_class=courseclass).annotate(num_books=Count('student'))
			# Group By Date Hour to compute attendance per class
		 	attendances = Attendance.objects.filter(course_class=courseclass)\
		 		.extra({'date':"strftime('%%d-%%m %%H', created_date)"})\
		 		.values('course_class','date')\
		 		.annotate(count=Count('student'))

		 	categories = []
		 	series = {'name':str(subject),'data':[]}
	 		
	 		for row in attendances:
	 			categories.append(str(row['date']))
	 			series['data'].append(row['count'])

	 		# Graph data
	 		context['categories'] = categories
	 		context['series'] = [series]

			context['classes'] = courseclass
			context['attendance'] = attendances



		


	return render(request,'basic/course_list.html',context=context)

# Create your views here.

class CourseAttendanceCount:
	course_name = ""
	attendance_count = 0
	student_id = ""
	student_parentno=""
	student_email=""
	student_name="Student"

	def to_dict(self):
		return {"student_id":str(self.student_id), "course_name":str(self.course_name),"attendance_count":str(self.attendance_count) }

	def _str_(self):
		return self.student_id + " " + self.course_name + " " + self.attendance_count


@csrf_exempt

def mark_attendance(request):

	rfid = request.POST.get("rfid","")
	#rfid="226545398"
	#deviceID="5"
	#time = request.POST.get("time", "")
	deviecID = request.POST.get("deviceID", "")

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
		room_d=MarkingUnit.objects.get(number=deviecID).room
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
	
	return HttpResponse(html)


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

def CalculateThreshold():
	localtime = time.localtime(time.time())
	yr = localtime.tm_year
	month = localtime.tm_mon
	semesterNumber = CheckEvenOdd(month)
	# Get Semester
	semester_d = Semester.objects.get(name=semesterNumber, year=yr)
	startTime=semester_d.start_time
	#print(startTime.date())
	#print(datetime.date.today())

	#d1 = datetime.strptime(startTime, "%Y-%m-%d")
	#d2 = datetime.strptime(datetime.date.today(), "%Y-%m-%d")

	noOfDays=(abs((startTime.date() - datetime.date.today()).days))
	weeks=noOfDays/7
	remainingDays=noOfDays%7
	classes=weeks*3 + remainingDays/2
	return ((classes*40)/100)


def SendMessageForAllStudentInAllCourses(request):
	StudentsCourseListToSendMesg=[]
	students = Student.objects.all()
	attendance_threshold = CalculateThreshold()
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

	#html = """<html><body>Marked Attendance for count {0} .</body></html>""".format(len(StudentsCourseListToSendMesg))
	html = StudentsCourseListToSendMesg
	Emails=[]
	if len(StudentsCourseListToSendMesg)>0:
		for stud in StudentsCourseListToSendMesg :
			#Emails.append(stud["student_email"])
			email_body = "Hello " + stud["student_name"] + "\n" + "You have low attendance in\n" + "Subject Name: "+stud["course_name"]+ "\n" + "Your attendance: "+ str(stud["attendance_count"])+ "\n"+"Minimum required (Upto today): "+ str(math.ceil(attendance_threshold))+ "\n"
			email_subject="Attendance Report - "+stud["course_name"]
			msg = EmailMultiAlternatives(subject=str(email_subject), body=str(email_body),
									 from_email="hello@naveenjaiswal.co",
									 to=[stud["student_email"]])
			msg.send()
			response = msg.mandrill_response[0]
	return JsonResponse(html,safe=False)


def SendMessageForStudent(request):
	student_id = request.POST.get("student_id", "")


def SendMessageForCourse(request):
	course_id = request.POST.get("course_name", "")

'''
def SendEmail11(request):
	send_mail('Put your Email subject here', 'Put your Email message here.', 'digvijaysingh073@gmail.com',['poojaruhal65@gmail.com'], fail_silently=False)
	html = """<html><body>Marked Attendance for count {0} .</body></html>""".format("done")
	return HttpResponse(html)
'''

def SendEmail(request):
	Emails = []
	Emails.append("h2015184@pilani.bits-pilani.ac.in")
	Emails.append("h2015171@pilani.bits-pilani.ac.in")
	msg = EmailMultiAlternatives(subject="Low attendance report", body="test body",
								 from_email="hello@naveenjaiswal.co",
								 to=Emails)
	msg.send()
	response = msg.mandrill_response[0]
	return HttpResponse(response)

class ColorsView(TemplateView):
    template_name = 'basic/colors.html'

    def get_context_data(self, **kwargs):
        data = super(ColorsView, self).get_context_data(**kwargs)
        data['colors'] = islice(next_color(), 0, 50)
        return data

class LineChartJSONView(BaseLineChartView):
	#template_name = 'templates/basic/line_chart.html'
    def get_labels(self):
        """Return 7 labels."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_data(self):
        """Return 3 dataset to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='basic/line_chart.html')
line_chart_json = LineChartJSONView.as_view()
colors = ColorsView.as_view()

