from django.urls import path
from .views import customer_dashboard, create_order, order_list, verify_order_completion, customer_profile, customer_profile_edit

app_name = 'customer'
urlpatterns = [
    path('dashboard/', customer_dashboard, name='dashboard'),
    path('create/', create_order, name='create_order'),
    path('orders/', order_list, name='order_list'),
    path('orders/verify/', verify_order_completion, name='verify_order_completion'),
    path('profile/', customer_profile, name='profile'),
    path('profile/edit/', customer_profile_edit, name='profile_edit'),
]
