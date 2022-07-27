from django.contrib import admin
from softdesk.models import Projects, Contributors, Issues, Comments


class ProjectsAdmin(admin.ModelAdmin):

    list_display = ("title", "description")


class ContributorsAdmin(admin.ModelAdmin):

    list_display = ("user_id", "role")


class IssuesAdmin(admin.ModelAdmin):

    list_display = ("title", "author_user_id")


class CommentsAdmin(admin.ModelAdmin):

    list_display = ("author_user_id", "description")


admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Contributors, ContributorsAdmin)
admin.site.register(Issues, IssuesAdmin)
admin.site.register(Comments, CommentsAdmin)
