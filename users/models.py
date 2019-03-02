from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create one to one relationship bewteen user and model
#CASCADE will delete profile if user is deleted.  
#But won't delete user if profile is deleted
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #add user photos to profile_pic directory
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	
	#__str__ tells how to print out
    def __str__(self):
        return f'{self.user.username} Profile'
    #runs after model saved
    def save(self, **kwargs):
        #save method of parent class
        super().save()
        #grab image that was saved from Pillow library and resize it	
        img = Image.open(self.image.path)
        #resize to smaller size if larger than 300	
        if img.height > 300 or img.width > 300:
            output_size = (300, 300) #max size tuple
            img.thumbnail(output_size)
            img.save(self.image.path)
