from django.db import models

class DataModel(models.Model):
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Data:: {self.id}"
