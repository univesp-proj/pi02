from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    #acrescentar os campos novos aqui
    #exemplo: bio = models.CharField(max_length=150, blank=True)

