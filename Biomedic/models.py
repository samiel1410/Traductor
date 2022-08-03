from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    codigo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entidad = models.TextField(max_length=200)
    grupo = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    def __str__(self):
        return self.codigo

    