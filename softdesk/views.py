from softdesk.models import Projects
from softdesk.serializers import ProjectsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

class ProjectsViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Projects.objects.all()

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)

    
class UserViewset(ReadOnlyModelViewSet):

    def get_queryset(self):
        return User.objects.all()
