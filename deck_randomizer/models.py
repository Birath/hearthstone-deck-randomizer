from django.db import models

# Create your models here.


class Card(models.Model):
    name = models.CharField(max_length=200)
    hero = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)
    dbfId = models.CharField(max_length=200)
    set = models.CharField(max_length=200)

    def __str__(self):
        return self.name
