from rest_framework import serializers
from collections import OrderedDict
from .models import Attribute, Product, ProductAttribute

class PricingSerializer(serializers.Serializer):
    """
    Serializer for the pricing details of the product.
    """
    selling_price = serializers.FloatField()
    min_order_quantity = serializers.IntegerField()
    max_order_quantity = serializers.IntegerField()
    incremental_quantity = serializers.IntegerField()


class ProductImageSerializer(serializers.Serializer):
    """
    Serializer for the images of the product.
    """
    title = serializers.CharField()
    alternate_text = serializers.CharField()
    sort_order = serializers.IntegerField()
    url_tiny = serializers.URLField()
    url_thumbnail = serializers.URLField()
    url_standard = serializers.URLField()
    url_zoom = serializers.URLField()


class AttributeSerializer(serializers.Serializer):
    """
    Serializer for the attributes of the product.
    """
    name = serializers.CharField()
    type = serializers.CharField()
    default_value = serializers.CharField()
    is_visibile = serializers.BooleanField()
    is_filterable = serializers.BooleanField()


class ProductReviewSerializer(serializers.Serializer):
    """
    Serializer for the reviews of the product.
    """
    product_id = serializers.IntegerField()
    rating = serializers.FloatField()
    review_text = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    status = serializers.CharField()
    is_featured = serializers.BooleanField()
    tags = serializers.JSONField()
    images = serializers.JSONField()
    videos = serializers.JSONField()
    review_date = serializers.DateTimeField()


class ProductSerializer(serializers.Serializer):
    """
    Serializer for the product details.
    Includes nested serializers for related fields: attributes, reviews, images, and pricing.
    """
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    short_description = serializers.CharField()
    product_type = serializers.CharField()
    active = serializers.BooleanField()
    sku = serializers.CharField()
    stock_available = serializers.BooleanField()
    is_featured = serializers.BooleanField()
    on_offer = serializers.BooleanField()
    on_subscription = serializers.BooleanField()
    on_promotion = serializers.BooleanField()
    has_variant = serializers.BooleanField()
    reviews_rating_sum = serializers.IntegerField()
    reviews_count = serializers.IntegerField()
    # attributes = AttributeSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(source='product_reviews', many=True)
    images = ProductImageSerializer(source='product_images', many=True)
    pricing = PricingSerializer(source='product_pricing', many=False)
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

    def to_representation(self, instance):
        """
        Overridden method to modify the output of the serializer.

        Splits the tags into a list if present.
        """
        data = super().to_representation(instance)
        if not instance.attribute_products.exists():
            data['attributes'] = []
        else:
            attribute_ids = ProductAttribute.objects.filter(
                product=instance).values_list('product_attribute', flat=True)
            attributes = Attribute.objects.filter(id__in=attribute_ids)
            serializer = AttributeSerializer(attributes, many=True)
            data['attributes'] = serializer.data
        return data


    def validate_sku(self, value):
        """
        Validate the SKU field. 
        Checks if SKU already exists. If it does, raises a validation error.
        """
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("SKU must be unique")
        return value
