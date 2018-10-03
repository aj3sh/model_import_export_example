import os

from django.shortcuts import render, HttpResponse
from django.views.generic import View

from .resources import BookResource
from .models import Book

class ExportBook(View):

	def get(self, request, *args, **kwargs):
		queryset = Book.objects.all()
		resource = BookResource(queryset)

		# creating documents directory
		if not os.path.exists('documents'):
			os.makedirs('documents')
		
		# saving excel files
		resource.to_excel('documents/test.xlsx')
		resource.to_excel('documents/test.xls')
		resource.to_csv('documents/test.csv')
		return HttpResponse('Success')