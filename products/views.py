from rest_framework import generics,permissions,status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer,UserRegistrationSerializer,UserLoginSerializer
from rest_framework.filters import SearchFilter,OrderingFilter
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.models import User

class ProductPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class DetailPagination(PageNumberPagination):
    page_size=1
    page_size_query_param = 'page_size'
    max_page_size = 100

# For creating new products
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    pagination_class = ProductPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name'] 
    ordering_fields = ['price', 'stock', 'created_at']

    def perform_create(self,serializer):
        serializer.save()
    
# For retrieving, updating and deleting products
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class=DetailPagination
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user) 
            return Response({'username': user.username, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user) 
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)