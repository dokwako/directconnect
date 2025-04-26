from django.urls import path
from .views import (
    admin_dashboard,
    order_assignment_view,
    assign_order,
    manage_users_view,
    all_orders_view,
    employee_reports_view,
    financial_summary_view,
    profile_view,
    add_employee_view,
    remove_employee_view,
)

app_name = 'adminpanel'
urlpatterns = [
    path('dashboard/', admin_dashboard, name='dashboard'),
    path('orders/assign/', order_assignment_view, name='order_assignment'),
    path('orders/assign/submit/', assign_order, name='assign_order'),
    path('users/manage/', manage_users_view, name='manage_users'),
    path('orders/all/', all_orders_view, name='all_orders'),
    path('reports/employees/', employee_reports_view, name='employee_reports'),
    path('reports/employees/add/', add_employee_view, name='add_employee'),
    path('reports/employees/remove/<int:user_id>/', remove_employee_view, name='remove_employee'),
    path('reports/financial/', financial_summary_view, name='financial_summary'),
    path('profile/', profile_view, name='profile'),
]
