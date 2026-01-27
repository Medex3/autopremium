import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosalon.settings')
django.setup()

from main.models import Car, News

# Добавить автомобили
cars_data = [
    {
        'brand': 'BMW', 'model': 'X5', 'year': 2023, 'price': 8500000,
        'body_type': 'suv', 'engine_volume': 3.0, 'horsepower': 340,
        'color': 'Чёрный', 'description': 'Премиальный кроссовер', 'is_available': True
    },
    {
        'brand': 'Mercedes', 'model': 'E-Class', 'year': 2024, 'price': 7200000,
        'body_type': 'sedan', 'engine_volume': 2.0, 'horsepower': 258,
        'color': 'Белый', 'description': 'Бизнес-класс', 'is_available': True
    },
    {
        'brand': 'Audi', 'model': 'A6', 'year': 2023, 'price': 6800000,
        'body_type': 'sedan', 'engine_volume': 2.0, 'horsepower': 245,
        'color': 'Серый', 'description': 'Немецкий седан', 'is_available': True
    }
]

for car_data in cars_data:
    Car.objects.get_or_create(
        brand=car_data['brand'],
        model=car_data['model'],
        year=car_data['year'],
        defaults=car_data
    )
    print(f"✅ Добавлен: {car_data['brand']} {car_data['model']}")

# Добавить новости
news_data = [
    {
        'title': 'Новая коллекция автомобилей 2024',
        'content': 'Представляем новую коллекцию премиальных автомобилей.',
        'excerpt': 'Обзор новых моделей',
        'is_published': True
    },
    {
        'title': 'Специальные предложения',
        'content': 'Только в этом месяце скидки на все модели.',
        'excerpt': 'Акции и скидки',
        'is_published': True
    }
]

for news_item in news_data:
    from django.utils.text import slugify

    news_item['slug'] = slugify(news_item['title'])

    News.objects.get_or_create(
        slug=news_item['slug'],
        defaults=news_item
    )
    print(f"✅ Добавлена новость: {news_item['title']}")

print("✅ Тестовые данные добавлены!")