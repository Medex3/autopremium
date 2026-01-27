import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosalon.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Создать/обновить администратора
user, created = User.objects.get_or_create(username='admin')
user.set_password('1111')
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

if created:
    print("✅ Администратор создан на Render")
else:
    print("✅ Пароль администратора обновлён на Render")

print("Логин: admin")
print("Пароль: 1111")