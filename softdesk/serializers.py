from rest_framework.serializers import ModelSerializer

from softdesk.models import Projects


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title']