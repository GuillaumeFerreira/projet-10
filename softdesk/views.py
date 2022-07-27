from softdesk.models import Projects, Contributors, Issues, Comments
from softdesk.serializers import (
    ProjectsSerializer,
    RegisterSerializer,
    ContributorsSerializer,
    ProjectsDetailSerializer,
    IssuesSerializer,
    CommentsSerializer,
    CommentsDetailSerializer,
    IssuesDetailSerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    DjangoObjectPermissions,
)
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User


class TestPerm(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == self.request.user)


class ProjectsViewset(ModelViewSet):

    serializer_class = ProjectsSerializer
    permission_classes = [TestPerm]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    detail_serializer_class = ProjectsDetailSerializer
    queryset = Projects.objects.all()

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(author_user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        content = {
            "user": str(request.user),  # `django.contrib.auth.User` instance.
            "auth": str(request.auth),  # None
            "status": "request was permitted",
        }
        return Response(content)


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Contributors.objects.all()

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        if user_id:
            contributor = Contributors.objects.get(
                project_id=self.kwargs["project_id"], user_id=user_id
            )
            self.kwargs["pk"] = contributor.id
        qs = super().get_queryset()
        return qs.filter(project_id=self.kwargs["project_id"])


class IssuesViewset(ModelViewSet):

    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated]
    queryset = Issues.objects.all()
    detail_serializer_class = IssuesDetailSerializer

    def get_queryset(self):

        qs = super().get_queryset()
        return qs.filter(project_id=self.kwargs["project_id"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["author_user_id"] = self.request.user
        context["project_id"] = Projects.objects.get(id=self.kwargs["project_id"])
        return context


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CommentsViewset(ModelViewSet):

    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]
    detail_serializer_class = CommentsDetailSerializer
    queryset = Comments.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["author_user_id"] = self.request.user
        context["issue_id"] = Issues.objects.get(id=self.kwargs["issue_id"])
        return context
