from django.contrib import admin
from .models import Storages


@admin.register(Storages)
class StoragesAdmin(admin.ModelAdmin):
    list_display = ('id', 'media_id', 'solution_id', 'report_id', 'type', 'recording')

    list_filter = ('type',)

    search_fields = ('id', 'media_id', 'solution_id', 'report_id')

    ordering = ('-id',)