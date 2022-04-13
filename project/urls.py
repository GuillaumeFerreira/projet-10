from django.contrib import admin
from django.urls import path, include
from softdesk.views import ProjectsAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/projects/', ProjectsAPIView.as_view())
]
