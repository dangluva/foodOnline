from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'country', 'city', 'pin_code']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Set these fields as optional
        self.fields['pin_code'].required = False
        self.fields['city'].required = False
        self.fields['country'].required = False
