from django.db import models
from django.contrib.auth.models import AbstractUser
import string, random 
# Create your models here.
class MainUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    matric_number = models.CharField(max_length=25)
    password = models.CharField(max_length=250)
    
    def __str__(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        if not self.matric_number:
            self.matric_number = "FTS/23/3210" + "".join(random.choices(string.digits, k=3))
        if self.password or not self.password:
            self.password = self.last_name
            self.set_password(self.last_name)
        return super().save(*args, **kwargs)
        
            