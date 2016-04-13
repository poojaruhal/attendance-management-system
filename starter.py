from django.contrib.auth.models import User

from basic.models import Faculty,Student,Department,Designation,Semester,Room

"""
Departments
"""
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

rooms = [6157,6155,6153]
for i in rooms:
	Room(number=str(i)).save()


###############################################################	

f_users = [
	["rahulbanerjee","Rahul","Banerjee","rahul@pilani.bits-pilani.ac.in","765","CSIS"],
	["ashishmishra","Ashish","Mishra","ashism@pilani.bits-pilani.ac.in","766","EEE"],
	["navneetgoel","Navneet","Goel","navneet@pilani.bits-pilani.ac.in","767","CSIS"],
	["poonamgoel","Poonam","Goel","poonam@pilani.bits-pilani.ac.in","768","CSIS"]
]

for user in f_users:
	
	department = Department.objects.filter(acronym=user[-1]).get()
	designation = Designation.objects.filter(acronym="Prof").get()

	user = User(username=user[0],password="coloring",first_name=user[1],last_name=user[2],email=user[3])
	faculty = Faculty(user=user,faculty_id=user[4],designation=designation,department=department)

###############################################################

s_users = [
	
	["h2015182","Sudhir","Mishra","h2015182@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
	["h2015184","Digvijay","Singh","h2015184@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
	["h2015183","Naveen","Jaiswal","h2015183@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
	["h2015171","Pooja","Ruhal","h2015171@pilani.bits-pilani.ac.in","$0012655434","CSIS"],
	["h2015116","Ravi","Shekhda","h2015116@pilani.bits-pilani.ac.in","$0012655434","EEE"],
	["h2015118","Chirag","Patel","h2015118@pilani.bits-pilani.ac.in","$0012655434","EEE"],
	
]

for user in s_users:
	
	department = Department.objects.filter(acronym=user[-1]).get()	

	user = User(username=user[0],password="coloring",first_name=user[1],last_name=user[2],email=user[3])
	student = Student(user=user,student_id=user[4],designation=designation,department=department)





"""
Email 

SendGrid

bf9d10355e4bd50d3fe4e932abffd6ba5b96eb44


curl \
-H "Content-Type: application/json" \
-H "Authorization: bf9d10355e4bd50d3fe4e932abffd6ba5b96eb44" \
-X POST -d '{"options":{"open_tracking":true,"click_tracking":true},"metadata":{"some_useful_metadata":"testing_sparkpost"},"substitution_data":{"signature":"Sudhir Mishra"},"recipients":[{"address":{"email":"sudhirxps@gmail.com"},"tags":["learning"],"substitution_data":{"customer_type":"Platinum","first_name":"Digvijay Singh"}}],"content":{"from":{"name":"Awesome Company","email":"sudhirxps@gmail.com"},"subject":"My first SparkPost Transmission","text":"Hi {{first_name}}\r\nYou have just sent your first email through SparkPost!\r\nCongratulations,\r\n{{signature}}","html":"<strong>Hi {{first_name}},</strong><p>You have just sent your first email through SparkPost!</p><p>Congratulations!</p>{{signature}}"}}' https://api.sparkpost.com/api/v1/transmissions

"""
