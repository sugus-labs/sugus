from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('names/<str:name>/', views.NameList.as_view()),
#    path('xxxx', views.xxxx, name = 'xxxx'),
]