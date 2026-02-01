from rest_framework import serializers, viewsets, permissions
from .models import ClassRoom
from django.contrib.auth.models import User


# -------------------------
# Serializer
# -------------------------
class ClassRoomSerializer(serializers.ModelSerializer):

    teacher = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )

    teacher_name = serializers.CharField(
        source="teacher.username",
        read_only=True
    )

    students = serializers.SerializerMethodField()

    subjects = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = ClassRoom
        fields = [
            "id",
            "name",
            "year",
            "teacher",
            "teacher_name",
            "students",
            "subjects",
        ]

    def get_students(self, obj):
        return [p.user.username for p in obj.students.all()]


# -------------------------
# Permission
# -------------------------
class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        profile = getattr(request.user, "profile", None)
        role = getattr(profile, "role", None)

        if request.method in permissions.SAFE_METHODS:
            return True

        return role in ["teacher", "admin"] or request.user.is_staff


# -------------------------
# ViewSet
# -------------------------
class ClassRoomViewSet(viewsets.ModelViewSet):

    queryset = (
        ClassRoom.objects
        .select_related("teacher")
        .prefetch_related("students__user", "subjects")
    )

    serializer_class = ClassRoomSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):

        user = self.request.user
        qs = self.queryset

        profile = getattr(user, "profile", None)
        role = getattr(profile, "role", None)

        if role == "student":
            return qs.filter(students__user=user)

        return qs
