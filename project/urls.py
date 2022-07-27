from django.contrib import admin
from django.urls import path, include
from softdesk.views import (
    ProjectsViewset,
    RegisterView,
    ContributorsViewset,
    IssuesViewset,
    CommentsViewset,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers


# Ici nous créons notre routeur
router = routers.SimpleRouter()
# afin que l’url générée soit celle que nous souhaitons ‘/projects/’
router.register(
    r"projects/(?P<project_id>[^/.]+)/users",
    ContributorsViewset,
    basename="contributors",
)
router.register("projects", ProjectsViewset, basename="projects")
router.register(
    r"projects/(?P<project_id>[^/.]+)/issues", IssuesViewset, basename="issues"
)
router.register(
    r"projects/(?P<project_id>[^/.]+)/issues/(?P<issue_id>[^/.]+)/comments",
    CommentsViewset,
    basename="comments",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("", include(router.urls)),
]
