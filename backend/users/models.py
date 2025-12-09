from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your model here
# AbstractUser = add/modify any fields. 
# AbstractBaseUser = we use this if you want to get the full control over your user model 
# BaseUserManager = Employee.objects = Manager

class User(AbstractUser):
    email = models.EmailField(unique=True)

    # Use email as the login field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # 'username' must still be required

    def __str__(self):
        return self.email