from django.db import models

# Create your models here.
class Moment(models.Model):
    content = models.CharField(max_length=200)
    user_name = models.CharField(max_length = 20)
    kind = models.CharField(max_length = 20)
