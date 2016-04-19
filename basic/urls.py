from django.conf.urls import url

from . import views
app = "basic"
urlpatterns = [

	url(r'^report$',views.report,name="report"),
    url(r'^mark_attendance$', views.mark_attendance),
    url(r'^$',views.index),
    url(r'^mark_attendance$', views.mark_attendance),
    url(r'^send_message', views.SendMessageForAllStudentInAllCourses),
    #url(r'^send_email', views.SendMessageForAllStudentInAllCourses),

]