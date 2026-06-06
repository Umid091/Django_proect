from django.contrib import admin
from .models import DataModel

@admin.register(DataModel)
class DataModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    search_fields = ('id',)