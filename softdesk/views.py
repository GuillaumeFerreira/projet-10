from softdesk.models import Projects, Contributors
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
    queryset = Projects.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author_user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
            'status': 'request was permitted'
        }
        return Response(content)

class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contributors.objects.all()

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        if user_id:
            contributor = Contributors.objects.get(project_id=self.kwargs['project_id'], user_id=user_id)
            self.kwargs['pk'] = contributor.id
        qs = super().get_queryset()
        return qs.filter(project_id=self.kwargs['project_id'])



class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
