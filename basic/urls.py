from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$',views.index)																																																																															,
	url(r'^faculty$',views.faculty),
    url(r'^mark_attendance$', views.mark_attendance),
    url(r'^send_message$', views.send_message),
]