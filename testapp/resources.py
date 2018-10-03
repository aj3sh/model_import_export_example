from model_import_export.resources import ModelResource, ForeignKeyResource, ManyToManyResource

from .models import *

class BookResource(ModelResource):
	#project = ForeignKeyResource(column='name')
	#per = ManyToManyResource(column='symbol')

	class Meta:
		model = Book
		fields = ['code', 'name', 'description']
		#exclude = ['created_by', 'created_at', 'deleted_at']