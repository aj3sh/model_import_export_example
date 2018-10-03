from django.db import models

class Book(models.Model):
	code = models.CharField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True)

	def __str__(self):
		return self.name