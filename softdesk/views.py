from softdesk.models import Projects
from softdesk.serializers import ProjectsSerializer, RegisterSerializer, ContributorsSerializer, ProjectsDetailSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User


class ProjectsViewset(ModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    detail_serializer_class = ProjectsDetailSerializer

    def get_queryset(self):
        return Projects.objects.filter(author_user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
            'status': 'request was permitted'
        }
        instance = generics.get_object_or_404(Projects, pk=ProjectsDetailSerializer.data['id'])
        print(instance)
        return Response(ProjectsDetailSerializer.data['id'])

    def get_serializer_class(self):
    # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
