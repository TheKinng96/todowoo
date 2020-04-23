from django.contrib import admin
from .models import Todo

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Todo, TaskAdmin)

