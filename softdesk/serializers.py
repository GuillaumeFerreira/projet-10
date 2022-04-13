from rest_framework.serializers import ModelSerializer

from softdesk.models import Projects


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title']