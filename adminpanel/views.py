import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from customer.models import Order
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db.models import Count, Q
from django.contrib import messages
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_revenue = Order.objects.filter(created_at__date=now().date()).aggregate(Sum('price'))['price__sum'] or 0
    total_users = get_user_model().objects.count()
    total_orders_today = Order.objects.filter(created_at__date=now().date()).count()
    pending_orders = Order.objects.filter(status='Pending').count()
    admin_name = request.user.get_full_name() or request.user.username

    context = {
        'total_revenue': total_revenue,
        'total_users': total_users,
        'total_orders_today': total_orders_today,
        'pending_orders': pending_orders,
        'admin_name': admin_name,
    }
    return render(request, 'adminpanel/dashboard.html', context)

@user_passes_test(is_admin)
def order_assignment_view(request):
    orders = Order.objects.filter(status='Pending')
    logger.info(f"Fetched {orders.count()} pending orders for assignment")
    employees = get_user_model().objects.filter(role='employee')
    context = {
        'orders': orders,
        'employees': employees,
    }
    return render(request, 'adminpanel/order_assign.html', context)

@user_passes_test(is_admin)
@require_POST
def assign_order(request):
    order_id = request.POST.get('order_id')
    employee_id = request.POST.get('employee_id')
    logger.debug(f"Assign order request received: order_id={order_id}, employee_id={employee_id}")
    if not order_id or not employee_id:
        messages.error(request, "Order and employee must be selected.")
        logger.warning("Order or employee ID missing in form submission.")
        return redirect('adminpanel:order_assignment')
    try:
        order = Order.objects.get(id=order_id, status='Pending')
        employee = get_user_model().objects.get(id=employee_id, role='employee')
    except Order.DoesNotExist:
        messages.error(request, "Order not found or not pending.")
        logger.error(f"Order not found or not pending: id={order_id}")
        return redirect('adminpanel:order_assignment')
    except get_user_model().DoesNotExist:
        messages.error(request, "Employee not found.")
        logger.error(f"Employee not found: id={employee_id}")
        return redirect('adminpanel:order_assignment')

    order.assigned_to = employee
    order.status = 'assigned'
    order.save()
    messages.success(request, f"Order {order.id} assigned to {employee.get_full_name() or employee.username}.")
    logger.info(f"Order {order.id} assigned to employee {employee.id}")
    return redirect('adminpanel:order_assignment')

@user_passes_test(is_admin)
def manage_users_view(request):
    User = get_user_model()
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'adminpanel/manage_users.html', context)

@user_passes_test(is_admin)
def all_orders_view(request):
    orders = Order.objects.all().select_related('customer', 'assigned_to')
    context = {
        'orders': orders,
    }
    return render(request, 'adminpanel/all_orders.html', context)

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse

from employee.models import Vehicle

@user_passes_test(is_admin)
def employee_reports_view(request):
    User = get_user_model()
    vehicles = Vehicle.objects.filter(in_use=False)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_vehicle_ids = request.POST.getlist('vehicles')
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('adminpanel:employee_reports')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('adminpanel:employee_reports')
        # Calculate next employee_id
        last_employee = User.objects.filter(role='employee').order_by('-employee_id').first()
        if last_employee and last_employee.employee_id and last_employee.employee_id.isdigit():
            next_employee_id = str(int(last_employee.employee_id) + 1)
        else:
            next_employee_id = '1000'
        assigned_vehicles = Vehicle.objects.filter(id__in=selected_vehicle_ids)
        vehicle_list_str = ','.join([v.plate_number for v in assigned_vehicles])
        user = User.objects.create_user(username=username, email=email, password=password, role='employee', employee_id=next_employee_id, assigned_vehicles=vehicle_list_str)
        user.save()
        # Mark vehicles as in use
        assigned_vehicles.update(in_use=True)
        messages.success(request, f"Employee {username} added successfully with Employee ID {next_employee_id}.")
        return redirect('adminpanel:employee_reports')

    employees = User.objects.filter(role='employee')
    employee_data = []
    for employee in employees:
        assigned_orders = Order.objects.filter(assigned_to=employee)
        orders_assigned = assigned_orders.filter(status='assigned').count()
        orders_in_transit = assigned_orders.filter(status='in_transit').count()
        orders_completed = assigned_orders.filter(status='delivered').count()
        employee_data.append({
            'employee': employee,
            'assigned_orders_count': orders_assigned,
            'in_transit_count': orders_in_transit,
            'completed_count': orders_completed,
            'assigned_vehicles': employee.assigned_vehicles or '-',
        })

    context = {
        'employee_data': employee_data,
        'vehicles': vehicles,
    }
    return render(request, 'adminpanel/employee_reports.html', context)

from employee.models import Vehicle
from customer.models import Order

@user_passes_test(is_admin)
def add_employee_view(request):
    User = get_user_model()
    vehicles = Vehicle.objects.filter(in_use=False)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        selected_vehicle_ids = request.POST.getlist('vehicles')
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return HttpResponseRedirect(reverse('adminpanel:add_employee'))
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return HttpResponseRedirect(reverse('adminpanel:add_employee'))
        # Calculate next employee_id
        last_employee = User.objects.filter(role='employee').order_by('-employee_id').first()
        if last_employee and last_employee.employee_id and last_employee.employee_id.isdigit():
            next_employee_id = str(int(last_employee.employee_id) + 1)
        else:
            next_employee_id = '1000'
        assigned_vehicles = Vehicle.objects.filter(id__in=selected_vehicle_ids)
        vehicle_list_str = ','.join([v.plate_number for v in assigned_vehicles])
        user = User.objects.create_user(username=username, email=email, password=password, role='employee', employee_id=next_employee_id, assigned_vehicles=vehicle_list_str)
        user.save()
        # Mark vehicles as in use
        assigned_vehicles.update(in_use=True)
        messages.success(request, f"Employee {username} added successfully with Employee ID {next_employee_id}.")
        return HttpResponseRedirect(reverse('adminpanel:employee_reports'))
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'adminpanel/add_employee.html', context)

@user_passes_test(is_admin)
def remove_employee_view(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id, role='employee')
        user.delete()
        messages.success(request, f"Employee {user.username} removed successfully.")
    except User.DoesNotExist:
        messages.error(request, "Employee not found.")
    return HttpResponseRedirect(reverse('adminpanel:employee_reports'))

@user_passes_test(is_admin)
def financial_summary_view(request):
    total_revenue = Order.objects.aggregate(Sum('price'))['price__sum'] or 0
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    assigned_orders = Order.objects.filter(status='assigned').count()
    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'assigned_orders': assigned_orders,
    }
    return render(request, 'adminpanel/financial_summary.html', context)

@user_passes_test(is_admin)
def profile_view(request):
    admin_user = request.user
    context = {
        'admin_user': admin_user,
    }
    return render(request, 'adminpanel/profile.html', context)
