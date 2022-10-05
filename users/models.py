from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.contrib.auth.models import PermissionsMixin
from .shortcuts import add_groups_to_user_by_roles
from django.contrib.postgres.fields import ArrayField


class StoreUserManager(BaseUserManager):
    def create_user(self, username, email, role, phone_number, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        add_groups_to_user_by_roles(user)
        if user.role == 'S':
            SellerProfile.objects.create(seller=user)
        elif user.role == 'B':
            BuyerProfile.objects.create(buyer=user)
            ShoppingCart.objects.create(buyer_profile=user.buyerprofile)
            Favourites.objects.create(buyer_profile=user.buyerprofile)
        return user

    def create_superuser(self, username, email, role, phone_number, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            role=role,
        )
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class StoreUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Username'
    )
    email = models.EmailField(
        max_length=255,
        verbose_name='Email',
        unique=True
    )

    class Roles(models.TextChoices):
        BUYER = 'B'
        SELLER = 'S'

    role = models.CharField(
        max_length=1,
        choices=Roles.choices,
        default=Roles.BUYER,
        verbose_name='Role',
    )

    phone_number = models.CharField(
        max_length=255,
        verbose_name='Phone number'
    )
    date_of_birth = models.DateTimeField(
        verbose_name='Your birthday',
        null=True
    )
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['username', 'role', 'phone_number']
    USERNAME_FIELD = 'email'

    objects = StoreUserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_seller(self):
        if self.role == 'S':
            return True
        return False

    @property
    def is_buyer(self):
        if self.role == 'B':
            return True
        return False

    @property
    def shoppingcart(self):
        if not self.is_buyer:
            raise AttributeError('Your model is not a buyer. It does not have shopping_cart attribute')
        return self.buyerprofile.shoppingcart

    @property
    def favourites(self):
        if not self.is_buyer:
            raise AttributeError('Your model is not a buyer. It does not have favourites attribute')
        return self.buyerprofile.favourites


class Address(models.Model):
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    postal_code = models.CharField(max_length=60)


class BuyerProfile(models.Model):
    buyer = models.OneToOneField(
        StoreUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    delivery_address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True
    )


class SellerProfile(models.Model):
    seller = models.OneToOneField(  # RENAME TO SELLER PROFILE
        StoreUser,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    company_name = models.CharField(
        max_length=40,
        null=True,  # remove this attribute
        default='',
    )


class ShoppingCart(models.Model):
    buyer_profile = models.OneToOneField(
        BuyerProfile,
        on_delete=models.CASCADE,
        primary_key=True
    )
    product_codes = ArrayField(
        models.PositiveBigIntegerField(),
        default=list,
    )
    # DELETE size and count


class Favourites(models.Model):
    buyer_profile = models.OneToOneField(
        BuyerProfile,
        on_delete=models.CASCADE,
        primary_key=True
    )
    product_codes = ArrayField(
        models.PositiveBigIntegerField(),
        default=list,
    )
