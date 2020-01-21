from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('item/<int:id>/', views.item, name='item'),
    path('signin/', views.signin, name='signin'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('save_favorites/', views.save_favorites, name='save_favorites'),
    path('my_favorites/', views.my_favorites, name='my_favorites'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('legal/', views.legal, name='legal')
]
