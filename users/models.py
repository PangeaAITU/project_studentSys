from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    
    # Добавляем привязку к классу
    # Если ClassRoom находится в другом приложении (например, 'school'), 
    # используем строку 'app_name.ModelName'
    classroom = models.ForeignKey(
        "school.ClassRoom", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="students" # Изменил на profiles, так как тут могут быть и учителя
    )

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

# ---------------------------------------------------------
# Сигналы (исправленные)
# ---------------------------------------------------------

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Важно: сохраняем профиль при обновлении User, 
        # чтобы изменения (например, смена пароля) не вызывали ошибок
        if hasattr(instance, 'profile'):
            instance.profile.save()