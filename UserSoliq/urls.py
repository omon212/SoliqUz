from django.urls import path
from .views import LogOutView,UserSoliqView,UserLoginView

urlpatterns = [
    path('logout/<str:refresh_token>/', LogOutView.as_view()),
    path('register/', UserSoliqView.as_view()),
    path('login/', UserLoginView.as_view())
]