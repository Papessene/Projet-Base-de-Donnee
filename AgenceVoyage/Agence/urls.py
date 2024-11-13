from . import views
from django.urls import path,include
from .views import home, login, register, liste_clients, reserver, visite

urlpatterns = [
    path('', home, name="home"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('clients/', liste_clients, name='liste_clients'),
    path('reserver/', reserver, name="reserver"),
    path('visite/', visite, name="visite"),
]
