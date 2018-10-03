from model_import_export.resources import ModelResource, ForeignKeyResource, ManyToManyResource, RelatedResource

from .models import *

class SubjectResource(ModelResource):
	class_obj = ForeignKeyResource(column='name')
	tags = ManyToManyResource(column='name')
	books = RelatedResource(column='name')

	class Meta:
		model = Subject
		fields = ['class_obj', 'code', 'name', 'tags', 'books']