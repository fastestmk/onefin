from django.db import models
from uuid import uuid4 
from django.contrib.auth.models import User

def generate_uuid():
    return str(uuid4())
# Create your models here.
class Movie(models.Model):
	uuid= models.UUIDField(primary_key = True, default = generate_uuid, editable = False)
	title = models.CharField(max_length=30)
	description = models.TextField()
	genre = models.CharField(max_length=30, blank=True, null=True, default="")

	def __str__(self):
		return self.title

class Collection(models.Model):
	uuid= models.UUIDField(primary_key = True, default = generate_uuid, editable = False)
	title = models.CharField(max_length=50, unique=True)
	description = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	movie = models.ManyToManyField(Movie)

	def __str__(self):
		return self.title