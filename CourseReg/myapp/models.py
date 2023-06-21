from django.db import models
from django.contrib.auth.models import AbstractUser
import string, random 
# Create your models here.
class Year(models.Model):
    LEVEL = (
        ("ND 1", "ND 1"),
        ("ND 2", "ND 2"),
        ("ND 3", "ND 3")
    )
    
    level = models.CharField(max_length=4, choices=LEVEL)
    
class MainUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    level = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
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
        if not self.username:
            random_username = "".join(random.choices(string.ascii_letters + string.digits, k=7))
            self.username = random_username
        return super().save(*args, **kwargs)
    

    
class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    
        
            