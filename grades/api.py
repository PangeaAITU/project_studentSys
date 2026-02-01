from rest_framework import serializers, viewsets, permissions
from django.contrib.auth.models import User
from .models import Grade

# -------------------------
# Serializer
# -------------------------
class GradeSerializer(serializers.ModelSerializer):
    # Используем StringRelatedField или CharField для отображения имен при чтении
    student = serializers.CharField(source="student.username", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    # Используем PrimaryKeyRelatedField для записи через ID
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="student",
        write_only=True
    )

    class Meta:
        model = Grade
        fields = [
            "id",
            "student",
            "student_id",
            "subject",      # Подразумевается ID предмета (если есть ForeignKey)
            "subject_name", # Название предмета текстом
            "value",
            "created_at",
        ]

# -------------------------
# Permission
# -------------------------
class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменение только учителям/админам. 
    Студенты могут только просматривать (SAFE_METHODS).
    """
    def has_permission(self, request, view):
        # 1. Проверяем, авторизован ли пользователь
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Получаем роль из профиля (используем .get на случай, если профиля нет)
        # Предполагаем наличие связи OneToOneField(User, related_name='profile')
        profile = getattr(request.user, "profile", None)
        role = getattr(profile, "role", None) if profile else None

        # 3. Логика прав
        if role == "student":
            return request.method in permissions.SAFE_METHODS
        
        # Учителя и админы проходят дальше
        return role in ["teacher", "admin"] or request.user.is_staff

# -------------------------
# ViewSet
# -------------------------
class GradeViewSet(viewsets.ModelViewSet):
    # Оптимизируем запросы через select_related, чтобы не было N+1
    queryset = Grade.objects.all().select_related("student", "subject")
    serializer_class = GradeSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def get_queryset(self):
        """
        Дополнительная логика: студент должен видеть только СВОИ оценки,
        а учитель — все.
        """
        user = self.request.user
        profile = getattr(user, "profile", None)
        role = getattr(profile, "role", None) if profile else None

        if role == "student":
            return self.queryset.filter(student=user)
        
        return self.queryset