from django.urls import path
from .views import AddCard,AddMoney ,PayMoneyWithCheck
urlpatterns = [
    path("addcard/",AddCard.as_view()),
    path("addmoney/",AddMoney.as_view()),
    path("createcheck/",PayMoneyWithCheck.as_view()),
]