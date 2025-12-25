from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from main.models import CustomUser, Car, News, Page


def create_groups_and_permissions():
    """Создание групп и назначение разрешений"""

    # 1. Группа Администраторы
    admin_group, created = Group.objects.get_or_create(name='Администраторы')
    if created:
        print("✅ Создана группа: Администраторы")

    # Даем все разрешения администраторам
    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    # 2. Группа Менеджеры
    manager_group, created = Group.objects.get_or_create(name='Менеджеры')
    if created:
        print("✅ Создана группа: Менеджеры")

    # Разрешения для менеджеров
    car_content_type = ContentType.objects.get_for_model(Car)
    news_content_type = ContentType.objects.get_for_model(News)
    page_content_type = ContentType.objects.get_for_model(Page)
    user_content_type = ContentType.objects.get_for_model(CustomUser)

    manager_permissions = Permission.objects.filter(
        content_type__in=[car_content_type, news_content_type, page_content_type],
        codename__in=['add', 'change', 'view', 'delete']
    )
    manager_group.permissions.set(manager_permissions)

    # 3. Группа Клиенты
    client_group, created = Group.objects.get_or_create(name='Клиенты')
    if created:
        print("✅ Создана группа: Клиенты")

    # Разрешения для клиентов (только просмотр)
    client_permissions = Permission.objects.filter(
        content_type__in=[car_content_type, news_content_type, page_content_type],
        codename__in=['view']
    )
    client_group.permissions.set(client_permissions)

    print("✅ Группы и разрешения созданы!")