from django.db import models


# Create your models here.
class Bot(models.Model):
    token = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    creation_date = models.DateField(auto_now_add=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name
