from django.urls import path, include
from blog import views

urlpatterns = [
    path('', views.article_list, name='articles'),
    path('tag/<slug:tag>/', views.tagview, name='tag'),
    path('<int:pk>', views.article_detail, name='article_detail')
]
