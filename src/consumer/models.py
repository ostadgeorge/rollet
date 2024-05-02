from django.db import models

# Create your models here.

class Wallet(models.Model):
    address = models.CharField(max_length=100)
    data = models.JSONField()

    def __str__(self):
        return self.address
