from django import forms
from employee.models import Vehicle

class DeliveryDetailsForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput())
    distance = forms.FloatField(label="Distance (km)", min_value=0)
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.filter(in_use=False), empty_label="Select Vehicle")
