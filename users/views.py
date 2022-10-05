from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

from .forms import (
    StoreUserSignUpForm,
)

from django.contrib.auth import login, authenticate


class StoreUserLogoutView(LogoutView):
    template_name = 'users/registration/logout.html'


class StoreUserLoginView(LoginView):
    template_name = 'users/registration/login.html'


def user_registration_view(request):
    context = dict()
    if request.method == 'POST':
        form = StoreUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = StoreUserSignUpForm()
    context['form'] = form
    return render(request, 'users/registration/signup.html', context=context)


@permission_required('users.view_buyerprofile')
def buyer_profile_view(request):
    authenticated_user = request.user
    print(authenticated_user.is_buyer)
    context = {
        'authenticated_user': authenticated_user,
    }
    return render(request, 'users/buyer_profile.html', context=context)


@permission_required('users.view_onsale')
def seller_profile_view(request):
    seller = request.user
    context = {
        'seller': seller,
    }
    return render(request, 'users/seller_profile.html', context=context)




