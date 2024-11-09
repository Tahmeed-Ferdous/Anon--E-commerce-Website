from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='user_profile/', default='def.png', null=True, blank=True)
    otp= models.TextField()
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    