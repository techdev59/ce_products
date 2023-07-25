from django.urls import path
from .views import ProductListApi, ProductRetrieveApi

urlpatterns = [
    path('', ProductListApi.as_view()),
    path('/<int:id>', ProductRetrieveApi.as_view()),
]
