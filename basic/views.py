from django.shortcuts import render
from django.http import HttpResponse
from basic.models import Student,Semester,Attendance,Course,CourseClass
from basic.models import Faculty
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):

	return render(request,'basic/welcome.html')

@login_required(login_url='/login/')
def faculty(request):

	# Allowd only for faculties

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