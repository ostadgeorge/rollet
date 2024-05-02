from django.db import models

# Create your models here.

class Wallet(models.Model):
    address = models.CharField(max_length=100, unique=True, primary_key=True, db_index=True)
    data = models.JSONField()

    def __str__(self):
        return self.address


class Config(models.Model):
    last_block = models.IntegerField()

    def __str__(self):
        return str(self.last_block)
