__all__ = ['SERIALIZER']


SERIALIZER = """from rest_framework.serializers import ModelSerializer
from . import models
{% for model in fields_dict %}

class {{ model.name }}Serializer(ModelSerializer):

    class Meta:
        model = models.{{ model.name }}{% if depth != 0 %}
        depth = {{ depth }}{% endif %}
        fields = ({% for field in model.fields %}
            {% if field == 'id' %}'pk'{% else %}'{{field}}'{% endif %},{% endfor %}
        )
{% endfor %}"""
