from django.db import models
from django.urls import reverse
from users.models import StoreUser


def user_directory_path(instance, filename):
    print(instance, type(instance))
    return f'{instance.seller.username}/{filename}'


class Product(models.Model): # RENAME TO PRODUCT
    product_code = models.PositiveBigIntegerField(
        unique=True
    )
    seller = models.ForeignKey(
        StoreUser,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=255,
    )
    weight = models.FloatField(
        default=0.0
    )
    product_description = models.TextField(
        max_length=400,
        help_text='Max symbols length is 400',
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    image = models.ImageField(
        upload_to=user_directory_path,
        null=True
    )
    color = models.CharField(
        max_length=30,
        default='non-color'
    )
    CATEGORY_CHOICES = (
        ('Hat', 'Hat'),
        ('Outwear', 'Outwear'),
        ('Shoes', 'Shoes'),
        ('Pants', 'Pants')
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='Outwear'
    )

    product_slug = models.SlugField(
        help_text='Use slug to define url name for your item',
        null=True,
        unique=True,
    )

    additional_information = models.CharField(
        max_length=500,
        verbose_name='Additional information',
        null=True,
        help_text='Add some information if you want'
    )

    is_on_sale = models.BooleanField(
        default=True,
    )

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={
            'product_slug': self.product_slug,
            'product_model_slug': self.product_model_slug}
                       )

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_product_model_slug(cls):
        return f'{cls.__name__.lower()}'

    @property
    def product_model_slug(self):
        return f'{self.__class__.__name__.lower()}'


class Sizes(models.Model):
    class Meta:
        abstract = True

    count = models.PositiveBigIntegerField(
        verbose_name='Number of items per size',
        default=0,
    )

    def __str__(self):
        return f'{self.size}: {self.count}'


class OutWear(Product):
    pass


class Shoes(Product):
    pass


class Hat(Product):
    pass


class Pants(Product):
    pass


class ShoesSizes(Sizes):
    CHOICES = ((str(shoe_size / 2), str(shoe_size / 2)) for shoe_size in range(6, 32))
    allowable_sizes = [str(shoe_size / 2) for shoe_size in range(6, 32)]
    size = models.CharField(
        max_length=10,
        choices=CHOICES
    )
    product = models.ForeignKey(
        Shoes,
        on_delete=models.CASCADE,
        verbose_name='Product'
    )


class OutWearSizes(Sizes):
    CHOICES = (
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL')
    )
    allowable_sizes = [choice[0] for choice in CHOICES]
    size = models.CharField(
        max_length=10,
        choices=CHOICES
    )
    product = models.ForeignKey(
        OutWear,
        on_delete=models.CASCADE
    )


class HatSizes(Sizes):
    CHOICES = (
        ('ONE SIZE', '50-58'),
    )
    allowable_sizes = ('ONE SIZE',)
    size = models.CharField(
        max_length=10,
        choices=CHOICES
    )
    product = models.ForeignKey(
        Hat,
        on_delete=models.CASCADE
    )


class PantsSizes(Sizes):
    CHOICES = (
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL')
    )
    allowable_sizes = [choice[0] for choice in CHOICES]
    size = models.CharField(
        max_length=10,
        choices=CHOICES
    )
    product = models.ForeignKey(
        Pants,
        on_delete=models.CASCADE,
    )
