from rest_framework.views import APIView
from rest_framework.response import Response
from softdesk.models import Projects
from softdesk.serializers import ProjectsSerializer


class ProjectsAPIView(APIView):

    def get(self, *args, **kwargs):
        projects = Projects.objects.all()
        serializer = ProjectsSerializer(projects, many=True)
        return Response(serializer.data)