from rest_framework.serializers import ModelSerializer
from softdesk.models import Projects, Contributors
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class ProjectsSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id', 'title','description','type']


    def create(self, validated_data, instance):


        projet = Projects.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
            author_user_id=instance.user.id
        )
        contributors = Contributors.objects.create(
            user_id=kwargs["user"],
            project_id=projet.id,

        )

        projet.save()
        contributors.save()

        return projet


class ContributorsSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'project_id', 'projects']

    def get_projets(self, instance):
        queryset = instance.projects.filter(user_id=self.request.user)
        serializer = ProjectsSerializer(queryset, many=True)
        return serializer.data

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user