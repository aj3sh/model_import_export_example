from model_import_export.resources import *

from .models import *

class SubjectResource(ModelResource):
	class_obj = ForeignKeyResource(column='name')
	author = OneToOneResource(column='name')
	tags = ManyToManyResource(column='name')
	books = RelatedResource(column='name')

	class Meta:
		model = Subject
		fields = ['class_obj', 'author', 'code', 'name', 'tags', 'books', 'date' , 'time', 'datetime']
		# fields = '__all__'
		# exclude = ['date', 'tags']