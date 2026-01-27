import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosalon.settings')
django.setup()

from django.contrib.auth.models import User

# Создаем или обновляем администратора
user, created = User.objects.get_or_create(username='admin')
user.set_password('Admin123!@#')  # Измените пароль!
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

if created:
    print("✅ Администратор создан")
else:
    print("✅ Права администратора обновлены")

print(f"Логин: admin")
print(f"Пароль: admin123")
