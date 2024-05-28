from django.contrib import admin

from .models import Answer, Category, Question

# Register your models here.
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Question)
