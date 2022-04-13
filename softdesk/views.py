from softdesk.models import Projects
from softdesk.serializers import ProjectsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class ProjectsViewset(ReadOnlyModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        return Projects.objects.filter(author_user_id=self.request.user)

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
            'status': 'request was permitted'
        }
        return Response(content)


