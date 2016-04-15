import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'ams'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ams.settings")

import django
django.setup()

from django.contrib.auth.models import User

from basic.models import Faculty,Student,Department,Course,CourseClass
from basic.models import Designation,Semester,Room, Time,Attendance

"""
Departments
"""
def create_departments():
	departments = [

		{'name':'Computer Science and Information Science','acronym':'CSIS'},
		{'name':'Electrical and Elertonics Engineering','acronym':'EEE'},

	]
	for department in departments:

		d = Department(name=department['name'],acronym=department['acronym'])
		d.save()

###############################################################

"""
Designation
"""
def create_designations():
	designations = [
		{'name':'Professor','acronym':'Prof'},
		{'name':'Associate Professor','acronym':'Asso Prof'},
		{'name':'Assitant Professor','acronym':'Asst Prof'},
		{'name':'Lecturer','acronym':'Lect'},
		{'name':'Assitant Lecturer','acronym':'Asst Lect'},
	]

	for designation in designations:

		d = Designation(name=designation['name'],acronym=designation['acronym'])
		d.save()

###############################################################

"""
Semester
"""

def create_semesters():
	semesters = [
		{
			'name':'even',
			'year':'2016'
		},
		{
			'name':'odd',
			'year':'2016'
		}
	]

	for semester in semesters:
		s = Semester(name=semester['name'],year=semester['year'])
		s.save()

###############################################################

"""
Time
"""
def create_time():
	time = [
		{
			'day':'monday',
			'hour':'18'
		},
		{
			'day':'tuesday',
			'hour':'20'
		},
	]
	for t in time:
		Time(day=t['day'],hour=t['hour']).save()

###############################################################

"""
Room
"""
def create_rooms():
	rooms = [6157,6155,6153]
	for i in rooms:
		Room(number=str(i)).save()


###############################################################	

def create_faculties():
	f_users = [
		["rahulbanerjee","Rahul","Banerjee","rahul@pilani.bits-pilani.ac.in","765","CSIS"],
		["ashishmishra","Ashish","Mishra","ashism@pilani.bits-pilani.ac.in","766","EEE"],
		["navneetgoel","Navneet","Goel","navneet@pilani.bits-pilani.ac.in","767","CSIS"],
		["poonamgoel","Poonam","Goel","poonam@pilani.bits-pilani.ac.in","768","CSIS"]
	]

	for f_user in f_users:
		
		department = Department.objects.filter(acronym=f_user[-1]).get()
		designation = Designation.objects.filter(acronym="Prof").get()

		user = User(username=f_user[0],password="coloring",first_name=f_user[1],last_name=f_user[2],email=f_user[3])
		user.save()
		faculty = Faculty(user=user,faculty_id=f_user[4],designation=designation,department=department)
		faculty.save()

###############################################################

def create_students():
	s_users = [
		
		["h2015182","Sudhir","Mishra","h2015182@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
		["h2015184","Digvijay","Singh","h2015184@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
		["h2015183","Naveen","Jaiswal","h2015183@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
		["h2015171","Pooja","Ruhal","h2015171@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
		["h2015116","Ravi","Shekhda","h2015116@pilani.bits-pilani.ac.in","$0012655434","EEE"],
		["h2015118","Chirag","Patel","h2015118@pilani.bits-pilani.ac.in","$0012655434","EEE"],
		
	]

	for s_user in s_users:
		
		department = Department.objects.filter(acronym=s_user[-1]).get()	

		user = User(username=s_user[0],
			password="coloring",
			first_name=s_user[1],
			last_name=s_user[2],
			email=s_user[3])
		user.save()
		student = Student(user=user,
			student_id=s_user[0],
			rf_id	=s_user[4],department=department,
			mobile_number="9983082156",
			parents_mobile_number="9983082156",
			parents_email=s_user[3]
			)
		student.save()

###############################################################

def create_course():
	
	courses = [
		["CSIS","Software Architechture","CSGS213"],
		["CSIS","Cloud Computing","CSGS215"],
		["EEE","VLSI Design","EEGS213"],
	]

	rahul = User.objects.filter(username="rahulbanerjee").get()
	ashish = User.objects.filter(username="ashishmishra").get()

	f1 = Faculty.objects.filter(user=rahul).get()
	f2 = Faculty.objects.filter(user=ashish).get()

	semester = Semester.objects.filter(year="2016",name="even").get()
	
	time_1 = Time.objects.filter(day="monday",hour="18").get()
	time_2 = Time.objects.filter(day="tuesday",hour="20").get()

	room = Room.objects.filter(number="6157").get()

	for course in courses:
		d = Department.objects.filter(acronym=course[0]).get()
		c = Course(name=course[1],department=d,code=course[2])
		c.save()

		if course[0] == "CSIS":
			f = f1
			t = time_1
		else:
			f = f2
			t = time_2

		class_1 = CourseClass(room=room,faculty=f,semester=semester,time=t,course=c)
		class_1.save()

def create_attendance():

	course_class = CourseClass.objects.all()

	students = Student.objects.all()

	for i in range(1,5):
		for course in course_class:
			for student in students:
				Attendance(course_class=course,student=student).save()





"""
Email 

SendGrid

bf9d10355e4bd50d3fe4e932abffd6ba5b96eb44


curl \
-H "Content-Type: application/json" \
-H "Authorization: bf9d10355e4bd50d3fe4e932abffd6ba5b96eb44" \
-X POST -d '{"options":{"open_tracking":true,"click_tracking":true},"metadata":{"some_useful_metadata":"testing_sparkpost"},"substitution_data":{"signature":"Sudhir Mishra"},"recipients":[{"address":{"email":"sudhirxps@gmail.com"},"tags":["learning"],"substitution_data":{"customer_type":"Platinum","first_name":"Digvijay Singh"}}],"content":{"from":{"name":"Awesome Company","email":"sudhirxps@gmail.com"},"subject":"My first SparkPost Transmission","text":"Hi {{first_name}}\r\nYou have just sent your first email through SparkPost!\r\nCongratulations,\r\n{{signature}}","html":"<strong>Hi {{first_name}},</strong><p>You have just sent your first email through SparkPost!</p><p>Congratulations!</p>{{signature}}"}}' https://api.sparkpost.com/api/v1/transmissions

"""
if __name__ == '__main__':
	# create_departments()
	# create_designations()
	# create_semesters()
	# create_time()
	# create_rooms()
	# create_faculties()
	# create_students()
	# create_course()
	create_attendance()

	"""
	print "\
	 1. Department \n \
	 2. Designation \n \
 	 2. Semester  \n \
	 3. Time  \n \
	 4. Room  \n \
	 5. Faculty  \n \
	 6. Student  \n \
	 "
	step = input("Enter step : ")
	
	function_step_mapping = {
		'0':'create_departments',
		'1':'create_designations',
		'2':'create_semesters',
		'3':'create_time',
		'4':'create_rooms',
		'5':'create_faculties',
		'6':'create_students',
	}

	if str(step) in function_step_mapping.keys():
		for key,value in function_step_mapping.iteritems()	:
			
			if int(key) >= int(step):
				print "Execute "+value
				try:
					globals()[value]()()
				except TypeError:
					print value
					
			else:
				print "Skipped "+value
	"""