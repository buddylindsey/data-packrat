from django.contrib import admin

from .models import DownloadTemplate, Attribute, TemplateAttribute
from .forms import AttributeForm

@admin.register(DownloadTemplate)
class DownloadTemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    form = AttributeForm

@admin.register(TemplateAttribute)
class TemplateAttributeAdmin(admin.ModelAdmin):
    pass