from django.db import models

class DateTimeModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False,)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True,)
	deleted_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		abstract = True

class Class(DateTimeModel):
	# foreignkey model
	name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.name


class Tag(DateTimeModel):
	# Many to many model
	name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.name


class Author(DateTimeModel):
	name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.name


class Subject(DateTimeModel):
	# Main model to be import/export
	class_obj = models.ForeignKey(Class, related_name='subjects', on_delete=models.CASCADE)
	author = models.OneToOneField(Author, null=True, blank=True)
	code = models.CharField(max_length=255, unique=True)
	name = models.CharField(max_length=255, unique=True)
	tags = models.ManyToManyField(Tag, related_name='subjects')
	date = models.DateField(null=True, blank=True)
	time = models.TimeField(null=True, blank=True)
	datetime = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.name


class Book(DateTimeModel):
	# Related model
	subject = models.ForeignKey(Subject, related_name='books', on_delete=models.CASCADE)
	code = models.CharField(max_length=255, unique=True)
	name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.name