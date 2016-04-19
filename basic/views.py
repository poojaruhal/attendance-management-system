from django.shortcuts import render
import datetime
from django.http import HttpResponse,JsonResponse
import time
import math
import json
from .models import Faculty
from enum import Enum
from .models import Student,Semester,Attendance,Course,CourseClass,MarkingUnit,Time,Room

import utils


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives

from random import randint
from django.views.generic import TemplateView

from itertools import islice
from django.db.models import Count


def index(request):
	return render(request,'basic/welcome.html')

@login_required(login_url='/login/')
def report(request):
	
	default_select = "Choose Subject"	
	subject = request.GET.get("subject",default=default_select) 

	request_faculty = Faculty.objects.filter(user=request.user)	

	request_student = Student.objects.filter(user=request.user)
	
	context = {}
	# TODO Move to a function
	localtime = time.localtime(time.time())
	yr=localtime.tm_year
	month=localtime.tm_mon
	hr=localtime.tm_hour			
	semesterNumber=utils.CheckEvenOdd(month)
	
	if semesterNumber == utils.SemesterNumber.odd:
		semesterNumber = "odd"
	elif semesterNumber == utils.SemesterNumber.even:
		semesterNumber = "even"

	# Get Semester
	semester = Semester.objects.filter(name=semesterNumber , year=yr)
		
	if request_faculty:
		
		request_faculty = request_faculty.get()
		courses = CourseClass.objects.filter(faculty=request_faculty)
		
		course_list = []

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

			
			# Selected Course
			course = Course.objects.filter(name=subject).get()


			# Group By Date Hour to compute attendance per class

			courseclass = CourseClass.objects.filter(semester=semester,course=course,faculty=request_faculty)
			attendances = Attendance.objects.filter(course_class=courseclass)\
		 		.extra({'date':"strftime('%%d-%%m %%H', created_date)"})\
		 		.values('course_class','date')\
		 		.annotate(count=Count('student'))			
		 	
		 	categories = []

	 		# Graph data

		 	series = {'name':str(subject),'data':[]}			

	 		for row in attendances:
	 			categories.append(str(row['date']))
	 			series['data'].append(row['count'])

	 		context['categories'] = categories
	 		context['series'] = [series]

	 		# Graph data ends

			context['classes'] = courseclass
			context['attendance'] = attendances

		return render(request,'basic/faculty_report.html',context=context)

	elif request_student:

		request_student = request_student.get()

		attendances = Attendance.objects\
				.values('course_class__course__name')\
				.filter(student=request_student,course_class__in=request_student.courseClass.all()).annotate(dcount=Count('course_class__course__name'))

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


		context['attendance'] = attendances
		context['total_classes'] = int(utils.getTotalClasses(semester))
		
		return render(request,'basic/student_report.html',context=context)

	

@csrf_exempt
def mark_attendance(request):

	rfid = request.POST.get("rfid","")
	#rfid="226545398"
	#deviceID="5"
	#time = request.POST.get("time", "")
	deviceID = request.POST.get("deviceID", "")

	html = Student.mark_attendance(rfid,deviceID)
	
	return HttpResponse(html)


def SendMessageForAllStudentInAllCourses(request):
	
	StudentsCourseListToSendMesg = Attendance.getStudentsWithLessAttendance()
	
	currentSemester = Semester.getCurrentSemesterNumber()
	attendance_threshold = utils.CalculateThreshold(currentSemester)

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
