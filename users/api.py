from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from .models import Profile


# -------------------------
# Serializer
# -------------------------
class StudentSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
    class_room = serializers.CharField(
        source="profile.class_room.name",
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "class_room",
        ]


# -------------------------
# ViewSet (CRUD автоматически)
# -------------------------
class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(profile__role="student")
    serializer_class = StudentSerializer
