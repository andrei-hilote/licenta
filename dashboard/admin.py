from django.contrib import admin
from .models import Temperature

@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'temperature', 'date')
    list_filter = ('type', 'date')
    search_fields = ('type', 'date')
    ordering = ('-date',)
