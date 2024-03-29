from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SimpleModel(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, null=True)

    class Meta:
        abstract = True
