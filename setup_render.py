# setup_render.py - ЕДИНЫЙ СКРИПТ ДЛЯ НАСТРОЙКИ
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosalon.settings')
django.setup()

from django.contrib.auth import get_user_model
from main.models import Car, News

User = get_user_model()

print("=" * 50)
print("НАСТРОЙКА RENDER")
print("=" * 50)

# 1. СОЗДАНИЕ АДМИНИСТРАТОРА
print("\n1. Настройка администратора...")
try:
    user = User.objects.get(username='admin')
    user.set_password('1111')
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print("✅ Пароль администратора обновлён")
except User.DoesNotExist:
    User.objects.create_superuser(
        username='admin',
        email='admin@autopremium.com',
        password='1111'
    )
    print("✅ Администратор создан")

print(f"   Логин: admin")
print(f"   Пароль: 1111")

# 2. ДОБАВЛЕНИЕ АВТОМОБИЛЕЙ
print("\n2. Добавление автомобилей...")

cars_data = [
    {
        'brand': 'BMW', 'model': 'X5', 'year': 2023, 'price': 8500000,
        'body_type': 'suv', 'engine_volume': 3.0, 'horsepower': 340,
        'color': 'Чёрный', 'description': 'Премиальный кроссовер в отличном состоянии',
        'is_available': True
    },
    {
        'brand': 'Mercedes-Benz', 'model': 'E-Class', 'year': 2024, 'price': 9200000,
        'body_type': 'sedan', 'engine_volume': 2.0, 'horsepower': 258,
        'color': 'Белый', 'description': 'Новый бизнес-седан с полным комплектом',
        'is_available': True
    },
    {
        'brand': 'Audi', 'model': 'A6', 'year': 2023, 'price': 7800000,
        'body_type': 'sedan', 'engine_volume': 2.0, 'horsepower': 245,
        'color': 'Серый металлик', 'description': 'Немецкое качество и комфорт',
        'is_available': True
    }
]

for car_data in cars_data:
    obj, created = Car.objects.get_or_create(
        brand=car_data['brand'],
        model=car_data['model'],
        year=car_data['year'],
        defaults=car_data
    )
    if created:
        print(f"✅ Добавлен: {car_data['brand']} {car_data['model']}")
    else:
        print(f"⚠️  Уже есть: {car_data['brand']} {car_data['model']}")

# 3. ДОБАВЛЕНИЕ НОВОСТЕЙ
print("\n3. Добавление новостей...")

news_items = [
    {
        'title': 'Открытие нового автосалона Premium Class',
        'content': 'Мы рады сообщить об открытии нашего нового автосалона Premium Class в центре города!',
        'excerpt': 'Открытие нового салона премиальных автомобилей',
        'is_published': True,
    },
    {
        'title': 'Специальная акция: Trade-in',
        'content': 'Только до конца месяца специальная программа Trade-in!',
        'excerpt': 'Выгодные условия обмена автомобиля',
        'is_published': True,
    }
]

for news_item in news_items:
    news_item['slug'] = slugify(news_item['title'])

    obj, created = News.objects.get_or_create(
        slug=news_item['slug'],
        defaults=news_item
    )
    if created:
        print(f"✅ Добавлена новость: {news_item['title']}")
    else:
        print(f"⚠️  Новость уже есть: {news_item['title']}")

print("\n" + "=" * 50)
print("✅ НАСТРОЙКА ЗАВЕРШЕНА")
print("=" * 50)
print(f"Всего автомобилей: {Car.objects.count()}")
print(f"Всего новостей: {News.objects.count()}")
print("\nАдминка: https://autopremium.onrender.com/admin/")
print("Сайт: https://autopremium.onrender.com/")