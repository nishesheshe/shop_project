from django.urls import path
from .views import (
    add_item_view,
    all_products_view,
    product_detail_view,
    select_category_to_add_product_view,
    edit_sizes_view,
    product_delete_view,
    product_edit_view,
    all_hats_view,
    all_outwear_view,
    all_pants_view,
    all_shoes_view,
    seller_products_on_sale_view,
    seller_shoes_on_sale_view,
    seller_pants_on_sale_view,
    seller_outwear_on_sale_view,
    seller_hats_on_sale_view,
    seller_withdrawn_from_sale_view,
    remove_product_from_sale,
    return_on_sale,
    add_to_shopping_cart,
    remove_from_shopping_cart,
    shopping_cart_view,
    buyer_favourites_view,
    add_to_favourites,
    remove_from_favourites,
)

urlpatterns = [
    # product CRUD
    path('select_category', select_category_to_add_product_view, name='select_category'),
    path('add_product/<slug:product_model_slug>', add_item_view, name='add_item'),
    path('catalogs/<slug:product_model_slug>/<slug:product_slug>', product_detail_view, name='item_detail'),
    path('edit_sizes/<slug:product_slug>', edit_sizes_view, name='edit_sizes'),
    path('delete_product/<slug:product_slug>', product_delete_view, name='product_delete'),
    path('edit_product/<slug:product_slug>', product_edit_view, name='product_edit'),
    # all products
    path('catalog/all_items', all_products_view, name='all_items'),
    path('catalog/hats', all_hats_view, name='all_hats'),
    path('catalog/outwear', all_outwear_view, name='all_outwear'),
    path('catalog/shoes', all_shoes_view, name='all_shoes'),
    path('catalog/pants', all_pants_view, name='all_pants'),
    # seller_profile
    path('users/seller_profile/products_on_sale', seller_products_on_sale_view, name='seller_products_on_sale'),
    path('users/seller_profile/shoes_on_sale', seller_shoes_on_sale_view, name='seller_shoes_on_sale'),
    path('users/seller_profile/pants_on_sale', seller_pants_on_sale_view, name='seller_pants_on_sale'),
    path('users/seller_profile/outwear_on_sale', seller_outwear_on_sale_view, name='seller_outwear_on_sale'),
    path('users/seller_profile/hats_on_sale', seller_hats_on_sale_view, name='seller_hats_on_sale'),
    path('users/seller_profile/withdrawn_from_sale', seller_withdrawn_from_sale_view, name='seller_withdrawn_from_sale'),
    # buyer_profile
    path('users/buyer_profile/shopping_cart', shopping_cart_view, name='shopping_cart'),
    path('users/buyer_profile/favourites', buyer_favourites_view, name='buyer_favourites'),
    # logic
    path('remove_from_on_sale/<slug:product_slug>', remove_product_from_sale, name='remove_product_from_sale'),
    path('return_on_sale/<slug:product_slug>', return_on_sale, name='return_on_sale'),
    path('add_to_shopping_cart/<slug:product_slug>', add_to_shopping_cart, name='add_to_shopping_cart'),
    path('remove_from_shopping_cart/<slug:product_slug>', remove_from_shopping_cart, name='remove_from_shopping_cart'),
    path('add_to_favourites/<slug:product_slug>', add_to_favourites, name='add_to_favourites'),
    path('remove_from_favourites/<slug:product_slug>', remove_from_favourites, name='remove_from_favourites')
]
