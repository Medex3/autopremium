# add_cars_simple.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosalon.settings')
django.setup()

from main.models import Car

cars = [
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

for car_data in cars:
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

print(f"\n✅ Всего автомобилей в базе: {Car.objects.count()}")