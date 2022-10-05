from django.contrib.auth.models import Group


def add_groups_to_user_by_roles(user):
    seller_group, created = Group.objects.get_or_create(name='Seller')
    buyer_group, created = Group.objects.get_or_create(name='Buyer')
    if user.role == 'S':
        user.groups.add(seller_group)
    elif user.role == 'B':
        user.groups.add(buyer_group)




