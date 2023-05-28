from django.db import models
import uuid

class Logins(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    username = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField(max_length=1000, null=True, blank=True)
    password1 = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    update_date = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

class Blacklist(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=True)
    username = models.ForeignKey(Logins, on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)
