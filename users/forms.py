from users.models import StoreUser, Favourites
from django.contrib.auth.forms import UserCreationForm
from users.shortcuts import (
    add_groups_to_user_by_roles,
)
from users.models import (
    SellerProfile,
    BuyerProfile,
    ShoppingCart,
)


class StoreUserSignUpForm(UserCreationForm):
    class Meta:
        model = StoreUser
        fields = ['username', 'email', 'role', 'phone_number']

    def save(self, commit=True):
        user = super().save()
        if user.role == 'B':
            buyer_profile = BuyerProfile.objects.create(buyer=user)
            ShoppingCart.objects.create(buyer_profile=buyer_profile)
            Favourites.objects.create(buyer_profile=buyer_profile)
            add_groups_to_user_by_roles(user)
            print(f'----------------{buyer_profile}')
        elif user.role == 'S':
            seller_profile = SellerProfile.objects.create(seller=user)
            add_groups_to_user_by_roles(user)
            print(f'----------------{seller_profile}')
        if commit:
            print(f'---------------At last user.save()')
            user.save()
        return user




