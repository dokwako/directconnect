from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('accounts:login'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('customer/', include(('customer.urls', 'customer'), namespace='customer')),
    path('employee/', include('employee.urls')),
    path('adminpanel/', include('adminpanel.urls')),
]
