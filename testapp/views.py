import os

from django.shortcuts import render, HttpResponse
from django.views.generic import View, TemplateView, ListView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from model_import_export.views import ResourceExport, ResourceImport

from .resources import SubjectResource
from .models import Subject


class SubjectView(ListView):
	model = Subject
	template_name = "testapp/subjects.html"
	context_object_name = 'subjects'

class ExportSubject(ResourceExport):
	resource_class = SubjectResource
	file_name = 'subjects'

	def get_queryset(self, *args, **kwargs):
		return Subject.objects.all().order_by('id')

class ImportSubject(ResourceImport):
	template_name = 'testapp/import.html'
	resource_class = SubjectResource
	file_name = 'subjects'
	success_url = reverse_lazy('testapp:subject')


class ExporttSubject(View):

	def get(self, request, *args, **kwargs):
		queryset = Subject.objects.all()
		resource = SubjectResource(queryset)

		# creating documents directory
		if not os.path.exists('documents'):
			os.makedirs('documents')
		
		# saving excel files
		resource.to_excel('documents/test.xlsx')
		return self.excel_response('documents/test.xlsx')

	def excel_response(self, file_name):
		file=open(file_name, "rb")
		content=file.read()
		response=HttpResponse(content)
		response['Content-Type']="application/xlsx"
		return response


class ImporttSubject(TemplateView):
	template_name = 'testapp/import.html'

	def post(self, request, *args, **kwargs):
		file_name = self.save_file(request)
		if not file_name:
			return HttpResponse('Invalid filename.')
		try:
			resource = SubjectResource()
			resource.from_excel('documents/test.xlsx')
			return HttpResponse(file_name+' saved and import successfully.<br><a href="/">Home page</a>')
		
		except Exception as e:
			return HttpResponse(str(type(e))+" "+str(e))

	def save_file(self, request, *args, **kwargs):
		fs = FileSystemStorage()

		# creating documents directory
		if not os.path.exists('documents'):
			os.makedirs('documents')

		# saving profile picture
		if request.FILES.get('import_file'):
			import_file = request.FILES.get('import_file')
			if not import_file.name.endswith('.xlsx'):
				return None
			os.remove('documents/test.xlsx')
			fs.save('documents/test.xlsx', import_file)
			return import_file.name

		return None

class ImportSubjectTest(TemplateView):

	def get(self, request, *args, **kwargs):
		resource = SubjectResource()
		resource.from_excel('documents/test.xlsx')
		return HttpResponse('Import success.')