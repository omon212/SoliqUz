from django.urls import path
from .views import AddCard,AddMoney
urlpatterns = [
    path("addcard/",AddCard.as_view()),
    path("addmoney/",AddMoney.as_view()),
]