import os

from django.shortcuts import render, HttpResponse
from django.views.generic import View, ListView

from .resources import SubjectResource
from .models import Subject


class SubjectView(ListView):
	model = Subject
	template_name = "testapp/subjects.html"
	context_object_name = 'subjects'

class ExportSubject(View):

	def get(self, request, *args, **kwargs):
		queryset = Subject.objects.all()
		resource = SubjectResource(queryset)

		# creating documents directory
		if not os.path.exists('documents'):
			os.makedirs('documents')
		
		# saving excel files
		resource.to_excel('documents/test.xlsx')
		resource.to_csv('documents/test.csv')
		return HttpResponse('Success')


class ImportSubject(View):

	def get(self, request, *args, **kwargs):
		resource = SubjectResource()
		
		# saving to model from excel files
		resource.from_csv('documents/test.csv')
		return HttpResponse('Success')