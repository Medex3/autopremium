from django.urls import path
from . import views

handler404 = 'main.views.custom_404'

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.cars_list, name='cars_list'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('contacts/', views.contacts, name='contacts'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('news/<slug:slug>/increment-views/', views.news_increment_views, name='news_increment_views'),
    path('search/', views.search, name='search'),
   ]