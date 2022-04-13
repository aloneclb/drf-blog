from django.urls import path
from . import views as api_view


app_name = 'members_api'

urlpatterns = [
    path('register/', api_view.UserCreateView.as_view(), name='user_register'),
]