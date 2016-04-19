from enum import Enum
import time
import datetime
class SemesterNumber(Enum):
	even = 1
	odd = 2

def CheckEvenOdd(month):

	if(month==1 & month==2 & month==3 & month==4 & month==5 & month==6) :
		return SemesterNumber.odd
	else :
		return SemesterNumber.even


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

	if (dayNo == 6):
		return "sunday"

def getTotalClasses(currentSemester):

	startTime=currentSemester.start_time
	#print(startTime.date())
	#print(datetime.date.today())

	#d1 = datetime.strptime(startTime, "%Y-%m-%d")
	#d2 = datetime.strptime(datetime.date.today(), "%Y-%m-%d")

	noOfDays=(abs((startTime.date() - datetime.date.today()).days))
	weeks=noOfDays/7
	remainingDays=noOfDays%7
	classes=weeks*3 + remainingDays/2
	return classes

def CalculateThreshold(currentSemester):
	classes = getTotalClasses(currentSemester)
	return ((classes*40)/100)

