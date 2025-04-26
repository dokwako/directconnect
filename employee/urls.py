from django.urls import path
from .views import employee_dashboard, assigned_orders, start_delivery, complete_delivery, employee_profile, delivery_details_view

app_name = 'employee'
urlpatterns = [
    path('dashboard/', employee_dashboard, name='dashboard'),
    path('assigned/', assigned_orders, name='assigned_orders'),
    path('start_delivery/', start_delivery, name='start_delivery'),
    path('complete_delivery/', complete_delivery, name='complete_delivery'),
    path('profile/', employee_profile, name='profile'),
    path('delivery_details/<int:order_id>/', delivery_details_view, name='delivery_details'),
]
