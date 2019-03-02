from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	#check timezone, post current time
	date_posted = models.DateTimeField(default=timezone.now)
	#if user is deleted delete post as well
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	#returns path to specific post instance so django can find individual post for edit/delete
	#reverse returns fullpath as a string, pk is primary key (instance of specific post)
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})