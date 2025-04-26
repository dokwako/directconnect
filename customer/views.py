from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order
from accounts.forms import UserProfileForm
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def customer_dashboard(request):
    user = request.user
    customer_name = user.get_full_name() or user.username
    recent_orders = Order.objects.filter(customer=user)
    in_transit_count = recent_orders.filter(status='in_transit').count()
    delivered_count = recent_orders.filter(status='delivered').count()
    context = {
        'customer_name': customer_name,
        'in_transit_count': in_transit_count,
        'delivered_count': delivered_count,
    }
    return render(request, 'customer/dashboard.html', context)

@login_required
def create_order(request):
    success = False
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()
            success = True
    else:
        form = OrderForm()
    return render(request, 'customer/create_order.html', {'form': form, 'success': success})

@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user).select_related('assigned_vehicle', 'assigned_to')
    return render(request, 'customer/order_list.html', {'orders': orders})

@login_required
@require_POST
def verify_order_completion(request):
    order_id = request.POST.get('order_id')
    try:
        order = Order.objects.get(id=order_id, customer=request.user, status='delivered', customer_verified=False)
    except Order.DoesNotExist:
        messages.error(request, "Order not found or cannot be verified.")
        return redirect('customer:order_list')
    order.customer_verified = True
    order.save()
    messages.success(request, f"Order {order.id} marked as verified by you.")
    return redirect('customer:order_list')

@login_required
def customer_profile(request):
    user = request.user
    return render(request, 'customer/profile.html', {'customer_user': user})

@login_required
def customer_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('customer:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'customer/profile_edit.html', {'form': form})
