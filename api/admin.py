from django.contrib import admin
from .models import Task

@admin.register(Task)
class AdminTask(admin.ModelAdmin):
    list_display = ['id','title','completed']
    list_per_page = 20
    list_filter = ["title"]