from django.urls import path
from .views import register, login, refresh

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('refresh/', refresh),
    # path('test/', test)
]
