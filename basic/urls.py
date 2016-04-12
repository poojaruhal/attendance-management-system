from django.conf.urls import url

from . import views

urlpatterns = [

	url(r'^faculty$',views.faculty,name="faculty"),
	url(r'^student$',views.student,name="student"),
    url(r'^mark_attendance$', views.mark_attendance),
    url(r'^$',views.index),
    url(r'^mark_attendance$', views.mark_attendance),
    url(r'^send_message', views.SendMessageForAllStudentInAllCourses),

]