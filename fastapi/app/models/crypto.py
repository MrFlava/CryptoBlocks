from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    name = models.CharField(max_length=50)

class Provider(models.Model):
    name = models.CharField(max_length=150)
    api_key = models.CharField(max_length=150)


class Block(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    block_number = models.IntegerField(default=0)
    providers = models.ManyToManyField(Provider, related_name="blocks")
    created_at = models.DateTimeField(auto_now_add=True)
    stored_at = models.DateTimeField(auto_now_add=True)