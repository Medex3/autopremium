from django.contrib import admin
from .models import Car, Page, News

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'price', 'is_available']
    list_filter = ['brand', 'is_available', 'body_type']
    search_fields = ['brand', 'model']

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_published', 'views']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Настройки', {
            'fields': ('is_published', 'views', 'created_at', 'updated_at')
        }),
    )