from django.db import models


class ProductManager(models.Manager):
    """
    Manager for product model.
    """

    def get_active_products(self):
        """
        Returns active products.
        """
        return self.filter(active=True)


class Product(models.Model):
    """
    Product model representing an item that can be purchased.
    """

    PHYSICAL = 'physical'
    DIGITAL = 'digital'
    PRODUCT_TYPES = (
        (PHYSICAL, 'Physical'),
        (DIGITAL, 'Digital'),
    )

    product_master_id = models.CharField(
        max_length=128, blank=True, null=True
    )
    name = models.CharField(max_length=128)
    sku = models.CharField(max_length=128, blank=True, null=True)
    product_type = models.CharField(
        max_length=128, choices=PRODUCT_TYPES,
        blank=True, null=True
    )
    active = models.BooleanField(default=True)
    stock_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    on_offer = models.BooleanField(default=False)
    on_subscription = models.BooleanField(default=False)
    on_promotion = models.BooleanField(default=False)
    has_variant = models.BooleanField(default=False)
    short_description = models.CharField(
        max_length=128, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    reviews_rating_sum = models.IntegerField(blank=True, null=True)
    reviews_count = models.IntegerField(blank=True, null=True)
    tags = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # Use custom manager
    objects = ProductManager()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """
    Attribute model representing product attributes.
    """
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=64, blank=True, null=True)
    default_value = models.CharField(max_length=64)
    is_visibile = models.BooleanField(default=True)
    is_filterable = models.BooleanField(default=True)
    is_required = models.BooleanField(default=True)
    is_localized = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"

    def __str__(self):
        return self.name




class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        related_name='attribute_products',
        null=True, blank=True
    )
    product_attribute = models.ForeignKey(
        Attribute, on_delete=models.SET_NULL,
        related_name='attributes',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    # guid = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        related_name='product_parent_category',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ProductCategory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        related_name='category_products',
        null=True, blank=True
    )
    product_category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='categories',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    title = models.CharField(max_length=128)
    alternate_text = models.CharField(max_length=128, blank=True, null=True)
    sort_order = models.IntegerField(blank=True, null=True)
    url_tiny = models.URLField(blank=True, null=True)
    url_thumbnail = models.URLField(blank=True, null=True)
    url_standard = models.URLField(blank=True, null=True)
    url_zoom = models.URLField(blank=True, null=True)
    other_details = models.JSONField(default=list, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_images'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ProductPricing(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE,
        related_name='product_pricing'
    )
    customer_group_id = models.CharField(max_length=128)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_quantity = models.IntegerField()
    max_order_quantity = models.IntegerField()
    incremental_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_reviews'
    )
    rating = models.DecimalField(
        max_digits=4, decimal_places=1,
        blank=True, null=True
    )
    review_text = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    tags = models.JSONField(default=list, blank=True, null=True)
    images = models.JSONField(default=list, blank=True, null=True)
    videos = models.JSONField(default=list, blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

