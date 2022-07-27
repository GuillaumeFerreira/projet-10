from django.db import models
from django.conf import settings


class Projects(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class Contributors(models.Model):

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name="projects_contributors"
    )
    # permission = models.ChoicesField()
    role = models.CharField(max_length=255)


class Issues(models.Model):

    title = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    project_id = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name="projects_issues"
    )
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    # assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)


class Comments(models.Model):

    description = models.TextField(blank=True)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    issue_id = models.ForeignKey(
        Issues, on_delete=models.CASCADE, related_name="issues"
    )
