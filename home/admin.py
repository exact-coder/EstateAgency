from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *

# Register your models here.

admin.site.register(Slider)

class PropertyModelAdmin(SummernoteModelAdmin):
    summernote_fields = 'description'

admin.site.register(Property, PropertyModelAdmin)
admin.site.register(Inquary)
