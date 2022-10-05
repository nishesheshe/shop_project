from django.views.generic import (
    TemplateView,
)

from .forms import (
    SelectCategoryForm,
)

from django.shortcuts import (
    render,
)

from django.http import (
    HttpResponseRedirect,
    HttpResponseNotFound,
)
from django.contrib.auth.decorators import permission_required

from django.urls import reverse

from .models import (
    Hat,
    OutWear,
    Pants,
    Shoes,
)
from .shortcuts import (
    get_all_products,
    get_product_by_slugs,
    get_product_sizes_manager,
    is_seller_owner,
    get_product_model_by_model_slug,
    get_product_creation_form,
    get_product_by_slug,
    is_product_has_sizes,
    get_product_sizes_inlineformset,
    get_sizes_creation_formset,
    get_sizes_creation_formset_default_initial,
    get_product_edit_form,
    add_to_on_sale,
    get_seller_products_on_sale,
    pop_from_on_sale,
    get_seller_shoes_on_sale,
    get_seller_pants_on_sale,
    get_seller_outwear_on_sale,
    get_seller_hats_on_sale,
    get_seller_withdrawn_from_sale,
    is_seller_owner_of_product,
    add_product_code_to_buyer_shopping_cart,
    is_product_in_shopping_cart,
    remove_product_code_from_buyer_shopping_cart,
    get_buyer_shopping_cart_products,
    add_product_to_buyer_favourites,
    pop_product_from_buyer_favourites,
    get_buyer_favourite_products,
    is_product_in_favourites,
)

from django.core.paginator import Paginator


# views
def all_products_view(request):
    contact_list = get_all_products()
    paginator = Paginator(contact_list, 15)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    last_page = paginator.num_pages - 1
    context = {
        'page_obj': page_obj,
        'last_page': last_page,
    }
    return render(request, 'store/all_items.html', context=context)


def all_hats_view(request):
    hats = Hat.objects.all()
    paginator = Paginator(hats, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    last_page = paginator.num_pages - 1
    context = {
        'page_obj': page_obj,
        'last_page': last_page,
    }
    return render(request, 'store/all_hats.html', context=context)


def all_outwear_view(request):
    outwear = OutWear.objects.all()
    paginator = Paginator(outwear, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    last_page = paginator.num_pages - 1
    context = {
        'page_obj': page_obj,
        'last_page': last_page,
    }
    return render(request, 'store/all_outwear.html', context=context)


def all_pants_view(request):
    pants = Pants.objects.all()
    paginator = Paginator(pants, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    last_page = paginator.num_pages - 1
    context = {
        'page_obj': page_obj,
        'last_page': last_page,
    }
    return render(request, 'store/all_pants.html', context=context)


def all_shoes_view(request, ):
    shoes = Shoes.objects.all()
    paginator = Paginator(shoes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    last_page = paginator.num_pages - 1
    context = {
        'page_obj': page_obj,
        'last_page': last_page,
    }
    return render(request, 'store/all_shoes.html', context=context)


def product_detail_view(request, product_model_slug, product_slug):
    product = get_product_by_slugs(product_model_slug, product_slug)
    product_sizes = get_product_sizes_manager(product).all()
    if hasattr(request.user, 'is_buyer') and request.user.is_buyer:
        shopping_cart_button_used = is_product_in_shopping_cart(request.user, product)
        favourites_button_used = is_product_in_favourites(request.user, product)
    else:
        shopping_cart_button_used = False
        favourites_button_used = False
    context = {
        'product': product,
        'product_sizes': product_sizes,
        'product_slug': product.product_slug,
        'shopping_cart_button_used': shopping_cart_button_used,
        'favourites_button_used': favourites_button_used,
    }
    return render(request, 'store/item_detail.html', context=context)


@permission_required('store.add_product')
def add_item_view(request, product_model_slug):
    product_model = get_product_model_by_model_slug(product_model_slug)
    product_creation_form = get_product_creation_form(product_model)
    if request.method == 'POST':
        product_creation_form = product_creation_form(
            request.POST,
            request.FILES,
            request=request,
            category_slug=product_model_slug
        )
        if product_creation_form.is_valid():
            product = product_creation_form.save()
            add_to_on_sale(request.user, product.product_code)  # add in seller on_sale collection product_code
            return HttpResponseRedirect(reverse('edit_sizes', kwargs={'product_slug': product.product_slug}))
    else:
        product_creation_form = product_creation_form(
            request=request,
            category_slug=product_model_slug
        )
    context = {
        'product_creation_form': product_creation_form,
        'category_slug': product_model_slug,
    }
    return render(request, 'store/add_item.html', context=context)


@permission_required('store.add_product')
def select_category_to_add_product_view(request):
    if request.method == 'POST':
        selected_category = request.POST['category'].lower()
        return HttpResponseRedirect(reverse('add_item', kwargs={'product_model_slug': selected_category}))
    else:
        select_category_form = SelectCategoryForm()
    context = {
        'select_category_form': select_category_form,
    }
    return render(request, 'store/select_category.html', context=context)


@permission_required('store.edit_sizes')
def edit_sizes_view(request, product_slug):
    product = get_product_by_slug(product_slug)
    if not is_seller_owner(request, product):
        return HttpResponseNotFound()
    if request.method == 'POST':
        if is_product_has_sizes(product):
            product_sizes_formset = get_product_sizes_inlineformset(product)
            product_sizes_formset = product_sizes_formset(request.POST, instance=product)
        else:
            product_sizes_formset = get_sizes_creation_formset(product)
            product_sizes_formset = product_sizes_formset(
                request.POST,
                initial=get_sizes_creation_formset_default_initial(product)
            )
        if product_sizes_formset.is_valid():
            for size_form in product_sizes_formset:
                size_form.save()
            return HttpResponseRedirect(reverse('item_detail', kwargs={
                'product_slug': product_slug,
                'product_model_slug': product.get_product_model_slug()
            }))
    else:
        if is_product_has_sizes(product):
            product_sizes_formset = get_product_sizes_inlineformset(product)
            product_sizes_formset = product_sizes_formset(instance=product)
        else:
            product_sizes_formset = get_sizes_creation_formset(product)
            product_sizes_formset = product_sizes_formset(initial=get_sizes_creation_formset_default_initial(product))
    context = {
        'product_sizes_formset': product_sizes_formset,
        'product_slug': product.product_slug,
    }
    return render(request, 'store/edit_product_sizes.html', context=context)


@permission_required('store.delete_product')
def product_delete_view(request, product_slug):
    product = get_product_by_slug(product_slug)
    if not is_seller_owner(request, product):
        return HttpResponseNotFound()
    delete_confirm_message = f'Are you sure you want to delete {product.title}?'
    if request.method == 'POST':
        if request.POST['delete']:
            pop_from_on_sale(request.user, product.product_code)
            product.delete()
        return HttpResponseRedirect(reverse('all_items'))
    else:
        return render(request, 'store/product_delete.html',
                      context={'delete_confirm_message': delete_confirm_message, 'product': product})


@permission_required('store.edit_product')
def product_edit_view(request, product_slug):
    product = get_product_by_slug(product_slug)
    if not is_seller_owner(request, product):
        return HttpResponseNotFound()
    product_edit_form_class = get_product_edit_form(product)
    if request.method == 'POST':
        product_edit_form = product_edit_form_class(request.POST, request.FILES, instance=product)
        if product_edit_form.is_valid():
            product_edit_form.save()
        return HttpResponseRedirect(reverse('all_items'))
    else:
        product_edit_form = product_edit_form_class(instance=product)
    context = {
        'product_edit_form': product_edit_form
    }
    return render(request, 'store/product_edit.html', context=context)

@permission_required('users.change_onsale')
def seller_products_on_sale_view(request):
    if not request.user.is_seller:
        return HttpResponseNotFound()
    products_on_sale = get_seller_products_on_sale(request.user)
    context = {
        'products_on_sale': products_on_sale,
    }
    return render(request, 'store/products_on_sale.html', context=context)

@permission_required('users.change_onsale')
def seller_shoes_on_sale_view(request):
    if not request.user.is_seller:
        return HttpResponseNotFound()
    shoes_on_sale = get_seller_shoes_on_sale(request.user)
    context = {
        'shoes_on_sale': shoes_on_sale,
    }
    return render(request, 'store/shoes_on_sale.html', context=context)

@permission_required('users.change_onsale')
def seller_pants_on_sale_view(request):
    if not request.user.is_seller:
        return HttpResponseNotFound()
    pants_on_sale = get_seller_pants_on_sale(request.user)
    context = {
        'pants_on_sale': pants_on_sale,
    }
    return render(request, 'store/pants_on_sale.html', context=context)

@permission_required('users.change_onsale')
def seller_outwear_on_sale_view(request):
    if not request.user.is_seller:
        return HttpResponseNotFound()
    outwear_on_sale = get_seller_outwear_on_sale(request.user)
    context = {
        'outwear_on_sale': outwear_on_sale,
    }
    return render(request, 'store/outwear_on_sale.html', context=context)

@permission_required('users.change_onsale')
def seller_hats_on_sale_view(request):
    if not request.user.is_seller:
        return HttpResponseNotFound()
    hats_on_sale = get_seller_hats_on_sale(request.user)
    context = {
        'hats_on_sale': hats_on_sale,
    }
    return render(request, 'store/hats_on_sale.html', context=context)

@permission_required('users.change_onsale')
def seller_withdrawn_from_sale_view(request):
    if not request.user.is_seller:
        return HttpResponseNotFound()
    withdrawn_from_sale = get_seller_withdrawn_from_sale(request.user)
    context = {
        'withdrawn_from_sale': withdrawn_from_sale,
    }
    return render(request, 'store/withdrawn_from_sale.html', context=context)


@permission_required('users.view_shoppingcart')
def shopping_cart_view(request):
    products = get_buyer_shopping_cart_products(request.user.shoppingcart)
    context = {
        'products': products,
    }
    return render(request, 'store/buyer_shopping_cart.html', context=context)


@permission_required('users.view_favourites')
def buyer_favourites_view(request):
    products = get_buyer_favourite_products(request.user)
    context = {
        'products': products,
    }
    return render(request, 'store/buyer_favourites.html', context=context)

@permission_required('users.change_onsale')
def remove_product_from_sale(request, product_slug):
    product = get_product_by_slug(product_slug)
    if request.method == 'POST' and is_seller_owner_of_product(request.user, product):
        product.is_on_sale = False
        product.save()
    return HttpResponseRedirect(reverse('seller_products_on_sale'))

@permission_required('users.change_onsale')
def return_on_sale(request, product_slug):
    product = get_product_by_slug(product_slug)
    if request.method == 'POST' and is_seller_owner_of_product(request.user, product):
        product.is_on_sale = True
        product.save()
    return HttpResponseRedirect(reverse('seller_withdrawn_from_sale'))


@permission_required('users.add_products_to_shopping_cart')
def add_to_shopping_cart(request, product_slug):
    if request.method == 'POST':
        product = get_product_by_slug(product_slug)
        buyer = request.user
        add_product_code_to_buyer_shopping_cart(buyer, product.product_code)
    return HttpResponseRedirect(reverse('item_detail', kwargs={'product_slug': product.product_slug,
                                                               'product_model_slug': product.product_model_slug}))


@permission_required('users.can_remove_product_from_shopping_cart')
def remove_from_shopping_cart(request, product_slug):
    if request.method == 'POST':
        product = get_product_by_slug(product_slug)
        buyer = request.user
        remove_product_code_from_buyer_shopping_cart(buyer, product.product_code)
    return HttpResponseRedirect(reverse('item_detail', kwargs={'product_slug': product.product_slug,
                                                               'product_model_slug': product.product_model_slug}))


@permission_required('users.add_to_favourites')
def add_to_favourites(request, product_slug):
    product = get_product_by_slug(product_slug)
    if request.user.is_buyer:
        add_product_to_buyer_favourites(request.user, product.product_code)
    else:
        return HttpResponseNotFound
    return HttpResponseRedirect(reverse('item_detail', kwargs={'product_slug': product.product_slug,
                                                               'product_model_slug': product.product_model_slug}))


@permission_required('users.remove_from_favourites')
def remove_from_favourites(request, product_slug):
    product = get_product_by_slug(product_slug)
    if request.user.is_buyer:
        pop_product_from_buyer_favourites(request.user, product.product_code)
    else:
        return HttpResponseNotFound()
    return HttpResponseRedirect(reverse('item_detail', kwargs={'product_slug': product.product_slug,
                                                               'product_model_slug': product.product_model_slug}))



