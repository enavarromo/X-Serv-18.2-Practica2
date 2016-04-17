from django.db import models

# Create your models here.

class urlLargas(models.Model):
    urlLarga = models.TextField(primary_key=True)
    urlCorta = models.TextField()
    
class urlCortas(models.Model):
    urlCorta = models.TextField(primary_key=True)
    urlLarga = models.TextField()
