from django.db import models


class Car(models.Model):
    BODY_TYPES = [
        ('sedan', 'Седан'),
        ('suv', 'Внедорожник'),
        ('coupe', 'Купе'),
        ('hatchback', 'Хэтчбек'),
    ]

    brand = models.CharField(max_length=50, verbose_name="Марка")
    model = models.CharField(max_length=50, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Год выпуска")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    body_type = models.CharField(max_length=20, choices=BODY_TYPES, verbose_name="Тип кузова")
    engine_volume = models.FloatField(verbose_name="Объем двигателя")
    horsepower = models.IntegerField(verbose_name="Лошадиные силы")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='cars/', verbose_name="Фото", blank=True)
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    content = models.TextField(verbose_name="Содержание")

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Мой сайт")
    description = models.TextField(default="Описание сайта")

    def __str__(self):
        return self.site_name


class News(models.Model):
    """Модель для новостей автосалона"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    content = models.TextField(verbose_name="Содержание")
    excerpt = models.TextField(max_length=300, verbose_name="Краткое описание", blank=True)
    image = models.ImageField(upload_to='news/', verbose_name="Изображение", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views = models.IntegerField(default=0, verbose_name="Просмотры")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматически создаем краткое описание из первых 200 символов
        if not self.excerpt and self.content:
            self.excerpt = self.content[:200] + '...' if len(self.content) > 200 else self.content
        super().save(*args, **kwargs)

