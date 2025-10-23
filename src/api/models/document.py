from django.db import models


class Document(models.Model):
    title: models.CharField = models.CharField(max_length=100)
    author: models.CharField = models.CharField(max_length=100)
    content: models.TextField = models.TextField()
    date: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    latitude: models.FloatField = models.FloatField(null=True, blank=True)
    longitude: models.FloatField = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title
