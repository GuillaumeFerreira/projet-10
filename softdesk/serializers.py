from rest_framework.serializers import ModelSerializer
from softdesk.models import Projects, Contributors, Issues, Comments
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class ProjectsSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type"]

    def create(self, validated_data):

        projet = Projects.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            type=validated_data["type"],
            author_user_id=self.context["request"].user,
        )

        projet.save()

        return projet


class ProjectsDetailSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ["id", "title", "description", "type"]


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ["user_id", "project_id", "id"]

    def validate(self, data):
        if Contributors.objects.filter(
            project_id=data["project_id"], user_id=data["user_id"]
        ).exists():
            raise serializers.ValidationError("User déjà dans les contributeurs")
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class IssuesSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ["id", "title", "desc", "project_id", "author_user_id"]
        read_only_fields = ["author_user_id", "project_id"]

    def create(self, validated_data):

        issue = Issues.objects.create(
            title=validated_data["title"],
            desc=validated_data["desc"],
            project_id=self.context["project_id"],
            author_user_id=self.context["author_user_id"],
        )
        issue.save()
        return issue


class IssuesDetailSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = [
            "id",
            "title",
            "tag",
            "priority",
            "status",
            "desc",
            "project_id",
            "author_user_id",
        ]


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "description"]
        read_only_fields = ["author_user_id", "issue_id"]

    def create(self, validated_data):

        comment = Comments.objects.create(
            description=validated_data["description"],
            issue_id=self.context["issue_id"],
            author_user_id=self.context["author_user_id"],
        )
        comment.save()
        return comment


class CommentsDetailSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ["id", "description", "issue_id", "author_user_id"]
