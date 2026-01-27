# fix_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosalon.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Создаём или обновляем администратора
try:
    user = User.objects.get(username='admin')
    user.set_password('1111')  # НОВЫЙ ПАРОЛЬ
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print("✅ Пароль администратора обновлён")
except User.DoesNotExist:
    User.objects.create_superuser(
        username='admin',
        email='admin@autopremium.com',
        password='1111'  # НОВЫЙ ПАРОЛЬ
    )
    print("✅ Администратор создан")

print("=== ДАННЫЕ ДЛЯ ВХОДА ===")
print("Сайт: https://autopremium.onrender.com/admin/")
print("Логин: admin")
print("Пароль: 1111")
print("=======================")