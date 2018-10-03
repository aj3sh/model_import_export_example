import os

from django.shortcuts import render, HttpResponse
from django.views.generic import View

from .resources import SubjectResource
from .models import Subject

class ExportSubject(View):

	def get(self, request, *args, **kwargs):
		queryset = Subject.objects.all()
		resource = SubjectResource(queryset)

		# creating documents directory
		if not os.path.exists('documents'):
			os.makedirs('documents')
		
		# saving excel files
		#resource.to_excel('documents/test.xlsx')
		#resource.to_excel('documents/test.xls')
		resource.to_csv('documents/test.csv')
		return HttpResponse('Success')