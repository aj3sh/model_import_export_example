from django.conf.urls import url
from . import views

app_name = 'testapp'

urlpatterns = [
	url(r'^export/subject$', views.ExportSubject.as_view(), name='subject'),
	url(r'^import/subject$', views.ImportSubject.as_view(), name='subject'),
]