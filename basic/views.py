from django.shortcuts import render
import datetime
from django.http import HttpResponse

from basic.models import Student,Semester,Attendance,Course,CourseClass
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def mark_attendance(request):

	rfid = request.POST.get("rfid","")

	if rfid:

		try:
			student = Student.objects.filter(rf_id=rfid).get()
			# Get the semester from the current data and time
			semester = Semester.objects.filter(name="Second").get()

			# Get the course from the current data and time and the reader_id
			course = Course.objects.filter(name="VLSI Design").get()

			courseclass = CourseClass.objects.filter(course=course.pk,semester=semester.pk).get()


			attendance = Attendance(course_class=courseclass,student=student)
			attendance.save()

			html = """<html><body>Marked Attendance for student {0} and course {1} .</body></html>""".format(student.user.username,courseclass.course.name)

		except :
			html = "Param error" 

	else:

		html = "<html><body>%s.</body></html>" % "No id passed"
	
	return HttpResponse(html)