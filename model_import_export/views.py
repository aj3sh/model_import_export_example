import os
import warnings

from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from model_import_export.forms import ImportForm

class ResourceExport(View):

	def get_queryset(self):
		return self.queryset

	def create_resource_path(self):
		# creating media directory
		if not os.path.exists('media'):
			os.makedirs('media')
		if not os.path.exists('media/excel'):
			os.makedirs('media/excel')

	def excel_response(self, file_name):
		file=open(file_name, "rb")
		content=file.read()
		response=HttpResponse(content)
		response['Content-Type']="application/xlsx"
		response['Content-Disposition'] = 'attachment; filename="'+str(self.file_name)+'.xlsx"'
		return response

	def get(self, request, *args, **kwargs):
		self.create_resource_path()
		resource = self.resource_class(self.get_queryset())
		resource.to_excel('media/excel/'+ str(self.file_name) +'.xlsx')
		return self.excel_response('media/excel/'+ str(self.file_name) +'.xlsx')

class ResourceImport(FormView):
	form_class = ImportForm
	file_input_name = 'file'

	def form_valid(self, form):
		if os.path.exists('media/excel/'+ str(self.file_name) +'.xlsx'):
			os.remove('media/excel/'+ str(self.file_name) +'.xlsx')
		fs = FileSystemStorage()
		file = form.cleaned_data[str(self.file_input_name)]
		if settings.MEDIA_ROOT:
			fs.save('excel/'+ str(self.file_name) +'.xlsx', file)
		else:
			print("MEDIA_ROOT not found in settings, saving excel files to `media` directory")
			fs.save('media/excel/'+ str(self.file_name) +'.xlsx', file)
		resource = self.resource_class()
		resource.from_excel('media/excel/'+ str(self.file_name) +'.xlsx')
		return super().form_valid(form)