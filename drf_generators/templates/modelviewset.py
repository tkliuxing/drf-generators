
__all__ = ['MODEL_URL', 'MODEL_VIEW']


MODEL_URL = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api


router = DefaultRouter()
{% for model in models %}
router.register(r'{{ model | lower }}', api.{{ model }}ViewSet){% endfor %}

urlpatterns = (
    path('api/v1/', include(router.urls)),
)
"""


MODEL_VIEW = """from rest_framework.viewsets import ModelViewSet
from . import serializers
from . import models
{% for model in models %}

class {{ model }}ViewSet(ModelViewSet):
    queryset = models.{{ model }}.objects.order_by('pk')
    serializer_class = serializers.{{ model }}Serializer
{% endfor %}"""
