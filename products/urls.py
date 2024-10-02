from django.urls import path
from .views import *
urlpatterns = [
    path('products/',ProductListCreateView.as_view()),
    path('products/<int:pk>/',ProductDetailView.as_view()),
    path('register/',UserRegistrationView.as_view()),
    path('login/',UserLoginView.as_view())
]

