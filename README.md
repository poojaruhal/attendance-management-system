# Attendance Mangement System #

Created in partial fulfillment of the course of Software for Embedded Systems

## Problem Statement ##

Use of RFID technology to record attendance in a typical school/college. Each student is provided with a unique RFID card, each classroom is equipped with a RFID reader, attendance is recorded for each student for each course every day. System generates various reports for carrying out student/course analysis based on the attendance.

## Getting Started ##

```
# Create virtual enviornment
virtualenv venv
source venv/bin/activate

# Install all required libraries
pip install -r requirements.txt

# Setup the default database
python manage.py migrate

# Create super user
python manage.py createsuperuser

# Run development server
python manage.py runserver 

```

## Team ##

* Digvijay Singh
* Pooja Ruhal
* Naveen Jaiswal
* Sudhir Mishra
