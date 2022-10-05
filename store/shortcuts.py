import sys

from django.core.exceptions import ObjectDoesNotExist

from store import categories_info
from store.models import Shoes, Hat, OutWear, Pants
from users.models import StoreUser


def get_all_products():
    """
    Get all_products from existing product models those described in categories_info module.
    returns list of all products.
    """
    all_products = []
    for product_class in categories_info.product_models:
        all_products += list(product_class.objects.all())
    return all_products


def get_products_on_page(page_number, items_per_page=16/4, order='title'):
    all_products = []
    products_slice = slice(page_number*items_per_page, page_number*items_per_page + items_per_page)
    for product_class in categories_info.product_models:
        all_products += list(product_class.objects.order_by(order)[products_slice])
    return all_products


def get_product_model_by_model_slug(product_model_slug):
    """
    :param product_model_slug: this slug is compared to model.category_slug
    :return: returns product model
    """
    for product_model in categories_info.product_models:
        if product_model_slug == product_model.get_product_model_slug():
            return product_model
    raise ValueError(f'Not found category by that slug {product_model_slug}')


def get_product_creation_form(product_model_class):
    """

    :param product_model_class: this function searches product creation form depends on product_model_class
    :return: returns product creation form
    """

    try:
        creation_form = getattr(
            sys.modules['store.forms'],
            categories_info.product_creation_forms[product_model_class.__name__]
        )
        return creation_form
    except AttributeError:
        print('Form not found. Check that your form is named as "product_model_name" + "CreationForm"')


def get_sizes_creation_formset(product):
    """
    Returns product creation formset by passed product.
    """
    try:
        creation_formset = getattr(
            sys.modules['store.forms'],
            categories_info.product_sizes_creation_formsets[product.__class__.__name__]
        )
        return creation_formset
    except AttributeError:
        print('Form not found. Check that your form variable is named as "model_name" + SizesCreationFormSet"')


def get_sizes_creation_formset_by_model_slug(product_model_slug):
    model = get_product_model_by_model_slug(product_model_slug)
    try:
        creation_formset = getattr(
            sys.modules['store.forms'],
            categories_info.product_sizes_creation_formsets[model.__name__]
        )
        return creation_formset
    except AttributeError:
        print('Form not found. Check that your form variable is named as "model_name" + SizesCreationFormSet"')


def get_product_sizes_manager(product):
    """
        Returns manager for product that can be used to get product sizes
        return example: product.outwearsizes_set
    """
    category_slug = get_product_category_slug(product)
    try:
        return getattr(product, category_slug + 'sizes_set')
    except AttributeError:
        print('manager_set not found. Check that your manager exists on name "model_name" + "_set"')


def get_product_sizes_model(product):
    """

    This function tries to find 'size_model' in models.py module
    via getattr(sys.modules['store.models'], size_model_name')
    Returns product size model.
    """
    product_sizes_model_name = get_product_model(product).__name__ + 'Sizes'
    try:
        return getattr(sys.modules['store.models'], product_sizes_model_name)
    except AttributeError:
        print('Class Model.__name__.Sizes not found. Check that your ModelSizes class named like "Model" + "Sizes"')


def get_allowable_sizes(product_sizes_model):
    """
    Returns product_model allowable sizes.
    """
    return product_sizes_model.allowable_sizes


def get_sizes_creation_formset_default_initial(product):
    """
    The function supplies sizes_creation_formset initial attribute by default data.
    """
    product_sizes_model = get_product_sizes_model(product)
    allowable_product_sizes = get_allowable_sizes(product_sizes_model)
    initial = [{'size': allowable_size, 'product': product, 'count': 0} for allowable_size in
               allowable_product_sizes]
    return initial


def get_existing_data_for_formset_sizes(product):
    """
    The function returns initial data with existing sizes on product.
    """
    product_sizes = get_product_sizes_manager(product).all()
    initial = [{'size': size.size, 'item_id': size.product, 'count': size.count} for size in product_sizes]
    return initial


def get_product_category_slug(product):
    return product.product_model_slug


def get_product_model(product):
    return product.__class__


def get_product_by_slug_disabled(product_slug):
    """
    This function compares passed argument product slug with product slugs on products
    from get_all_products().
    Returns product if found compare.
    """
    for product in get_all_products():
        if product.product_slug == product_slug:
            return product
    raise ValueError('Check slug. You should pass only existing slug')


def get_product_by_slug(product_slug):
    """
    Finds a product by product_slug.
    :param product_slug: Unique value so objects.filter can return only one value with that slug
    :return: product
    """
    for product_model in categories_info.product_models:
        product = product_model.objects.filter(product_slug=product_slug).first()
        if product is not None:
            return product
    raise ObjectDoesNotExist(f'Not found product with slug "{product_slug}"')

# TRY TO OPTIMIZE THOSE QUERIES
def get_product_by_code(product_code):
    for product_model in categories_info.product_models:
        product = product_model.objects.filter(product_code=product_code).first()
        if product is not None:
            return product
    raise ObjectDoesNotExist(f'Not found product with product_code "{product_code}"')


def get_product_by_slugs(product_model_slug, product_slug):
    """
    Find a product by product_model_slug and product_slug.
    :param product_model_slug: product_model_slug is necessary to find a product model
    :param product_slug: after we found product model we use product_slug in product_model.objects.get
    :return:
    """
    product_model = get_product_model_by_model_slug(product_model_slug)
    return product_model.objects.get(product_slug=product_slug)


def get_product_sizes_inlineformset(product):
    product_sizes_inlineformset_name = get_product_sizes_model(product).__name__ + 'InlineFormSet'
    try:
        return getattr(sys.modules['store.forms'], product_sizes_inlineformset_name)
    except AttributeError:
        print('InlineFormSet not found. Check that your form variable is named as "model_name" + "SizesInlineFormSet"')


def get_product_sizes(product):
    return get_product_sizes_manager(product).all()


def get_product_edit_form(product):
    product_edit_form_name = get_product_model(product).__name__ + 'EditForm'
    try:
        return getattr(sys.modules['store.forms'], product_edit_form_name)
    except AttributeError:
        print('Check that you have edit form named as "model_name" + "EditForm"')


def is_product_has_sizes(product):
    if get_product_sizes_manager(product).all():
        return True
    return False


def get_product_count(product):
    product_sizes = get_product_sizes_manager(product).all()
    count = 0
    for size in product_sizes:
        count += size.count
    return count


def is_seller_owner(request, product):
    return request.user == product.seller


def get_seller_on_sale(seller_user):
    return seller_user.sellerprofile.onsale


def add_to_on_sale(seller_user, product_code):
    on_sale = get_seller_on_sale(seller_user)
    on_sale.product_codes.append(product_code)
    on_sale.save()
    print(on_sale.product_codes)
    return 1


def pop_from_on_sale(seller_user, product_code):
    on_sale = get_seller_on_sale(seller_user)
    pop_index = on_sale.product_codes.index(product_code)
    on_sale.product_codes.pop(pop_index)
    on_sale.save()
    return 1


def get_seller_products_on_sale(seller):
    return list(Hat.objects.filter(seller=seller, is_on_sale=True)) + list(OutWear.objects.filter(seller=seller, is_on_sale=True )) + list(
        Pants.objects.filter(seller=seller, is_on_sale=True)) + list(Shoes.objects.filter(seller=seller, is_on_sale=True))


def get_products_on_sale_codes(seller_user):
    on_sale = get_seller_on_sale(seller_user)
    products_on_sale_codes = on_sale.product_codes
    return products_on_sale_codes


def get_model_products_on_page(product_model, page_number, order='title', items_per_page=15):
    """
    :param order: string that describes order of return products
    :param items_per_page: defines how many items will be received for page
    :param product_model:
    :param page_number: is a number from 0 to n
    :return: products on page
    """
    products_slice = slice(page_number * items_per_page, page_number * items_per_page + items_per_page)
    products_on_page = product_model.objects.order_by(order)
    return products_on_page[products_slice]


def get_seller_products_on_sale_by_model(seller, product_model=None):
    if product_model is None:
        raise ValueError(f'Invalid product_model {product_model}. You must use model of your product.')
    return product_model.objects.filter(seller=seller, is_on_sale=True)


def get_seller_shoes_on_sale(seller):
    shoes_on_sale = Shoes.objects.filter(seller=seller, is_on_sale=True)
    return shoes_on_sale


def get_seller_pants_on_sale(seller):
    pants_on_sale = Pants.objects.filter(seller=seller, is_on_sale=True)
    return pants_on_sale

def get_seller_outwear_on_sale(seller):
    outwear_on_sale = OutWear.objects.filter(seller=seller, is_on_sale=True)
    return outwear_on_sale


def get_seller_hats_on_sale(seller):
    hats_on_sale = Hat.objects.filter(seller=seller, is_on_sale=True)
    return hats_on_sale


def get_seller_withdrawn_from_sale(seller):
    return list(Hat.objects.filter(seller=seller, is_on_sale=False)) + \
        list(OutWear.objects.filter(seller=seller,  is_on_sale=False)) + \
        list(Pants.objects.filter(seller=seller, is_on_sale=False)) + \
        list(Shoes.objects.filter(seller=seller, is_on_sale=False))


def is_seller_owner_of_product(seller, product):
    if product.seller == seller:
        return True
    return False


def add_product_code_to_buyer_shopping_cart(buyer, product_code):
    shopping_cart = buyer.shoppingcart
    shopping_cart.product_codes.append(product_code)
    print(shopping_cart.product_codes)
    shopping_cart.save()
    return 1


def remove_product_code_from_buyer_shopping_cart(buyer, product_code):
    shopping_cart = buyer.shoppingcart
    index_to_pop = shopping_cart.product_codes.index(product_code)
    shopping_cart.product_codes.pop(index_to_pop)
    shopping_cart.save()
    print(f'POP {shopping_cart}')
    return 1


def is_product_in_shopping_cart(buyer, product):
    if product.product_code in buyer.shoppingcart.product_codes:
        return True
    return False


def get_buyer_shopping_cart_products(shopping_cart):
    product_codes = shopping_cart.product_codes
    products = [get_product_by_code(product_code) for product_code in product_codes]
    return products


def add_product_to_buyer_favourites(buyer, product_code):
    favourites = buyer.favourites
    favourites.product_codes.append(product_code)
    favourites.save()
    print(f'FAVOURITES CODES{favourites.product_codes}')
    return 1


def pop_product_from_buyer_favourites(buyer, product_code):
    favourites = buyer.favourites
    index_to_pop = favourites.product_codes.index(product_code)
    favourites.product_codes.pop(index_to_pop)
    favourites.save()
    print(f'FAVOURITE CODES{favourites.product_codes}')
    return 1


def get_buyer_favourite_products(buyer):
    favourite_products = [get_product_by_code(product_code) for product_code in buyer.favourites.product_codes]
    return favourite_products


def is_product_in_favourites(buyer, product):
    if product.product_code in buyer.favourites.product_codes:
        return True
    return False



