from django.db import models

# Django User Model
from django.contrib.auth.models import User

class File(models.Model):
	# users that can access the file
	users = models.ManyToManyField(User)
	file_name = models.CharField(max_length=50)
	# file_path filed can be added here

	def __str__(self):
		return self.file_name


