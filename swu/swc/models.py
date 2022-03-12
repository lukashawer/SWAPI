from django.utils.timezone import now
from django.db import models

# Create your models here.
class Document(models.Model):
    date = models.DateTimeField("retrieving date", default=now)
    filename = models.FileField(upload_to='edoc/%Y/%m/', blank=True, null=True,)
    description = models.CharField("Description", max_length=200, default='', blank=True)
