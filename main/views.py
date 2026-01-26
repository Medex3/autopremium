from django.shortcuts import render, get_object_or_404
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import json
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import Car, News, Page
from django.urls import path
from . import views


def home(request):
    # Берем 6 последних автомобилей для главной
    new_cars = Car.objects.filter(is_available=True).order_by('-id')[:6]

    # Берем 3 последние новости для главной
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]

    return render(request, 'home.html', {
        'new_cars': new_cars,
        'latest_news': latest_news,
    })

def cars_list(request):
    Car = apps.get_model('main', 'Car')

    # Получаем все доступные автомобили
    cars = Car.objects.filter(is_available=True)

    # Фильтрация по типу кузова
    body_type = request.GET.get('body_type')
    if body_type:
        cars = cars.filter(body_type=body_type)

    # Получаем отображаемое название типа кузова для активного фильтра
    active_filter = body_type if body_type else ''
    filter_display = dict(Car.BODY_TYPES).get(body_type, '') if body_type else ''

    return render(request, 'cars.html', {
        'cars': cars,
        'active_filter': active_filter,
        'filter_display': filter_display,
        'body_types': Car.BODY_TYPES
    })


def car_detail(request, car_id):
    Car = apps.get_model('main', 'Car')
    car = get_object_or_404(Car, id=car_id)

    return render(request, 'car_detail.html', {'car': car})


def page_detail(request, slug):
    Page = apps.get_model('main', 'Page')
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'page.html', {'page': page})


def sitemap(request):
    Page = apps.get_model('main', 'Page')
    Car = apps.get_model('main', 'Car')

    pages = Page.objects.all()
    body_types = Car.BODY_TYPES

    return render(request, 'sitemap.html', {
        'pages': pages,
        'body_types': body_types
    })


def custom_404(request, exception):
    context = {
        'error_message': str(exception) if str(exception) else 'Страница не найдена',
        'request_path': request.path,
    }
    return render(request, '404.html', context, status=404)

def contacts(request):
    """Страница контактов"""
    return render(request, 'contacts.html')


def news_list(request):
    """Список всех новостей"""
    News = apps.get_model('main', 'News')

    # Получаем опубликованные новости
    news_list = News.objects.filter(is_published=True)

    # Пагинация - 6 новостей на странице
    paginator = Paginator(news_list, 6)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return render(request, 'news_list.html', {
        'news_list': news,
        'page_obj': news,
        'is_paginated': paginator.num_pages > 1,
    })


def news_detail(request, slug):
    """Детальная страница новости"""
    News = apps.get_model('main', 'News')

    news = get_object_or_404(News, slug=slug, is_published=True)

    # Получаем похожие новости (последние 3)
    similar_news = News.objects.filter(
        is_published=True
    ).exclude(
        id=news.id
    ).order_by('-created_at')[:3]

    return render(request, 'news_detail.html', {
        'news': news,
        'similar_news': similar_news,
    })


@require_POST
@csrf_exempt
def news_increment_views(request, slug):
    """Увеличение счетчика просмотров (AJAX)"""
    News = apps.get_model('main', 'News')

    try:
        news = News.objects.get(slug=slug)
        news.views += 1
        news.save()
        return JsonResponse({'status': 'success', 'views': news.views})
    except News.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


# Обновите функцию home для отображения новостей на главной
def home(request):
    Car = apps.get_model('main', 'Car')
    News = apps.get_model('main', 'News')

    # Берем 6 последних автомобилей
    new_cars = Car.objects.filter(is_available=True).order_by('-id')[:6]

    # Берем 3 последние новости для главной
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:3]

    return render(request, 'home.html', {
        'new_cars': new_cars,
        'latest_news': latest_news,
    })


def search(request):
    """ Поиск по сайту"""
    query = request.GET.get('q', '').strip()
    results = {
        'cars': [],
        'news': [],
        'pages': [],
        'query': query,
        'has_results': False
    }

    if query:
        # Ищем в автомобилях
        Car = apps.get_model('main', 'Car')
        results['cars'] = Car.objects.filter(
            is_available=True
        ).filter(
            models.Q(brand__icontains=query) |
            models.Q(model__icontains=query) |
            models.Q(description__icontains=query)
        )[:10]  # Ограничиваем 10 результатами

        # Ищем в новостях
        News = apps.get_model('main', 'News')
        results['news'] = News.objects.filter(
            is_published=True
        ).filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(excerpt__icontains=query)
        )[:10]

        # Ищем в страницах
        Page = apps.get_model('main', 'Page')
        results['pages'] = Page.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query)
        )[:10]

        # Проверяем, есть ли результаты
        results['has_results'] = any([
            results['cars'].exists(),
            results['news'].exists(),
            results['pages'].exists()
        ])

    return render(request, 'search_results.html', results)


