from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^faculty$',views.faculty),
    url(r'^mark_attendance$', views.mark_attendance),
]