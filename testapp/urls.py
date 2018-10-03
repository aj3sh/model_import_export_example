from django.conf.urls import url
from . import views

app_name = 'testapp'

urlpatterns = [
	url(r'^export/book$', views.ExportBook.as_view(), name='book'),
]