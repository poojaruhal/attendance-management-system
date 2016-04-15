from django.conf.urls import url

from . import views

urlpatterns = [

	url(r'^faculty$',views.faculty,name="faculty"),
	url(r'^student$',views.student,name="student"),
    url(r'^mark_attendance$', views.mark_attendance),
    url(r'^$',views.index),
    url(r'^mark_attendance$', views.mark_attendance),
    url(r'^send_message', views.SendMessageForAllStudentInAllCourses),
    #url(r'^send_email', views.SendMessageForAllStudentInAllCourses),
    url(r'^threshold', views.CalculateThreshold),


    #url(r'^linechart', views.LineChartJSONView.as_view(), name='results'),
    url(r'^line_chart/$', views.line_chart,
        name='line_chart'),
    url(r'^line_chart/json/$', views.line_chart_json,
        name='line_chart_json'),
    url(r'^colors/$', views.colors, name='colors'),

]