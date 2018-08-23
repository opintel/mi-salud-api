from django.db import models


# Create your models here.
class Bot(models.Model):
    token = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    creation_date = models.DateField(auto_now_add=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class HistoricalMessage(models.Model):
    message = models.CharField(max_length=500)
    message_date = models.CharField(max_length=150)
    flow = models.CharField(max_length=150)
    model_tag = models.CharField(max_length=150, null=True)
    user_tag = models.CharField(max_length=150, null=True)
    id_message = models.IntegerField()
    id_rp_user = models.IntegerField()
    id_bot = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.id_message, self.flow, self.message_date)
