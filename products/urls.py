from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('products/',ProductListCreateView.as_view()),
    path('products/<int:pk>/',ProductDetailView.as_view()),
    path('register/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

