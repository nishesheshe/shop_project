from django.urls import path
from .views import (
    StoreUserLogoutView,
    user_registration_view,
    buyer_profile_view,
    StoreUserLoginView,
    seller_profile_view,
)
app_name = 'user'
urlpatterns = [
    path('login/', StoreUserLoginView.as_view(), name='login'),
    path('signup/', user_registration_view, name='signup'),
    path('logout/', StoreUserLogoutView.as_view(), name='logout'),
    path('buyer_profile/', buyer_profile_view, name='buyer_profile'),
    path('seller_profile/', seller_profile_view, name='seller_profile')
]
