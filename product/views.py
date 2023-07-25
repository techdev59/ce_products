from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

from .pagination import CustomLimitOffsetPagination

class ProductListApi(generics.ListAPIView):
    """
    ProductListApi is a view for handling 'list' actions. It uses
    Django REST framework's ListAPIView for listing all products.

    It prefetches related fields 'attributes', 'product_reviews', 
    and 'product_categories' for better performance.

    CustomLimitOffsetPagination is used for paginating the results.
    """


    queryset = Product.objects.all().prefetch_related(
        'attribute_products', 'product_reviews', 'category_products')
  
    serializer_class = ProductSerializer
    pagination_class = CustomLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        """
        Overridden method of ListAPIView to provide custom response format.

        Returns the list of products and pagination details.
        """
        response = super().list(request, *args, **kwargs)
        pagination = response.data.pop('pagination')
        results = response.data.pop('results')

        # Set up the response data
        response.data['message'] = 'Products retrieved successfully.'
        response.data['success'] = True
        response.data['content'] = {
            'products': results,
            'pagination': pagination
        }

        return response


class ProductRetrieveApi(generics.RetrieveUpdateDestroyAPIView):
    """
    ProductRetrieveApi is a view for handling 'retrieve', 'update' 
    and 'destroy' actions for a single product instance identified by ID.

    It prefetches related fields 'attributes', 'product_reviews', 
    and 'product_categories' for better performance.
    """

 
    queryset = Product.objects.all().prefetch_related(
        'attribute_products', 'product_reviews', 'category_products')
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get(self, request, id):
        """
        Overridden method of RetrieveUpdateDestroyAPIView to provide 
        custom response format for GET requests.

        Returns the details of a single product instance.
        """
        queryset = self.get_queryset().filter(id=id)
        serializer = self.serializer_class(queryset.first())
        data = serializer.data

        return Response({
            'message': 'Product retrieved successfully.',
            'success': True,
            'content': {'product': data}
            }, status=status.HTTP_200_OK)
