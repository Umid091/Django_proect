
from django.db import models


class Storages(models.Model):
    RECORDING_TYPE = [
        ('full', 'Full'),
        ('part', 'Part'),
    ]

    recording = models.FileField(upload_to='recordings/%Y/%m/%d', null=True, blank=True)
    media_id = models.IntegerField(null=True, blank=True,)
    solution_id = models.IntegerField(null=True, blank=True)
    report_id = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=RECORDING_TYPE, default='part')

