__all__ = ['ADMIN']


ADMIN = """from django.contrib import admin
from . import models
{% for model in fields_dict %}

@admin.register(models.{{model.name}})
class {{ model.name }}Admin(admin.ModelAdmin):
    list_display = [{% for field in model.fields %}{% if field == 'id' %}'pk'{% else %}'{{field}}'{% endif %}, {% endfor %}]
{% endfor %}"""
