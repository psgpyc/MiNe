from django.urls import path
from . import views

app_name = 'userextended'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create-user'),
    path('token/', views.CreateTokenView.as_view(), name='token-user'),
    path('me/', views.ManageUserView.as_view(), name='me-user'),


]
