import pandas as pd

from django.db.models import Count

class ModelResource:
	"""
	Model resources:
	Exports queryset of model into excel and csv file
	And import excel or csv file data into model
	"""

	def __init__(self, queryset=None):
		"""
		Initializing model resource
		Input: queryset (not required)
		"""

		self.__list = None
		if queryset != None:
			self.__process_queryset(queryset)
		del queryset


	def __get_fields(self):
		"""
		-- IMPORT EXPORT --
		Returns list of fields for resource
		"""

		# print(self.Meta.model._meta.fields)
		fields = self.Meta.fields
		if 'id' not in fields:
			fields.insert(0, 'id')
		return fields


	def __get_database_fields(self):
		"""
		-- IMPORT EXPORT --
		Returns list of database fields (normal, foreign, related, m2m) for values
		"""
		fields = self.__get_fields() # getting all fields
		db_fields = list()	# database list to be appended
		temp_attr = None

		for field in fields:
			if hasattr(self, field):	# checking if field has attribute (special field)
				temp_attr = getattr(self, field)
				if type(temp_attr) == ForeignKeyResource:
					db_fields.append([field, 'foreign'])
				elif type(temp_attr) == RelatedResource:
					db_fields.append([field, 'related'])
				elif type(temp_attr) == ManyToManyResource:
					db_fields.append([field, 'm2m'])
			else:
				db_fields.append([field, 'normal'])

		return db_fields


	def __process_queryset(self, queryset):
		"""
		-- EXPORT --
		Process queryset into dictionary list that is to be saved
		"""
		db_fields = self.__get_database_fields()	# categoried resource fields wrt db
		
		self.__fields_values = list()	# fields values to be converted in list before renaming and converted to dataframe 
		self.__rename_values = dict()	# foreign key to be rename from 'project__column' to 'project'
		annotate_dict = dict()	# queryset annotate fields for m2m and related fields 
		queryset_values = list()	# queryset values names
				
		for db_field in db_fields:

			if db_field[1] == 'normal':
				# normal field (just add to queryset_values and fields_values)
				self.__fields_values.append( db_field[0] )
				queryset_values.append( db_field[0] )
			
			elif db_field[1] == 'foreign':
				# foreignkey field ( add to queryset_values, fields_values and rename_values)
				self.__fields_values.append( db_field[0] + '__' + getattr(self, db_field[0]).column )
				queryset_values.append( db_field[0] )
				self.__rename_values[db_field[0] + '__' + getattr(self, db_field[0]).column ] = db_field[0]
			
			else:
				# m2m and related fields ( add to fields_values, postprocess_fields and annotate_dict to take just count as its column)
				self.__fields_values.append(db_field[0])
				annotate_dict[db_field[0]] = Count(db_field[0])

		# gettings values from queryset		
		self.__list = list(queryset.order_by('id').values(*queryset_values).annotate(**annotate_dict).values(*self.__fields_values))

		# appending one to many fields to list
		o2m_field = self.__get_o2m_field(db_fields, queryset)
		for i in range(0, len(self.__list)):
			for field in o2m_field[self.__list[i]['id']]:
				self.__list[i][field] = o2m_field[self.__list[i]['id']][field]

		del queryset


	def __get_o2m_field(self, db_fields, queryset):
		"""
		returns o2m and related queryset
		"""

		postprocess_fields = [ db_field[0] for db_field in db_fields if db_field[1] == 'related' or db_field[1] == 'm2m' ]
		o2m_field = dict()
		for obj in queryset:
			o2m_field[obj.id] = dict()
			for field in postprocess_fields:
				texts = [ getattr(m2m_obj, getattr(self, field).column) for m2m_obj in getattr(obj, field).all() ]
				o2m_field[obj.id][field] = ",".join(texts)

		return o2m_field


	def __check_queryset(self):
		"""
		-- EXPORT --
		Checks if queryset is available or not before exporting
		"""

		if self.__list == None:
			raise Exception('Cannot export without queryset.')


	def __get_dataframe(self):
		"""
		-- EXPORT --
		returns dataframe from the list
		"""
		self.__check_queryset()
		df = pd.DataFrame(self.__list, columns=self.__fields_values)
		df=df.rename(columns = self.__rename_values)
		print(df)
		return df


	def to_excel(self, file_name):
		"""
		saves queryset to respective excel file
		"""
		self.__get_dataframe().to_excel(file_name, index=False)

	def to_csv(self, file_name):
		"""
		saves queryset to respective csv file
		"""
		self.__get_dataframe().to_csv(file_name, index=False)



class ForeignKeyResource:
	"""
	Foreign key resource
	Used for foriegnkey field in model resource
	"""

	def __init__(self, **kwargs):
		if kwargs.get('column'):
			self.column = kwargs.get('column')
		else:
			self.column = 'id'

class RelatedResource:
	"""
	Related resource for realted names
	One to many relations
	"""

	def __init__(self, **kwargs):
		if kwargs.get('column'):
			self.column = kwargs.get('column')
		else:
			self.column = 'id'

class ManyToManyResource:
	"""
	Many to Many resource
	Used for many to many field in model resource
	"""

	def __init__(self, **kwargs):
		if kwargs.get('column'):
			self.column = kwargs.get('column')
		else:
			self.column = 'id'