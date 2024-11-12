from django import forms
from .models import Request
from .models import Vendor
from django.core.exceptions import ValidationError

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            'vendor_name',
            'type_of_vendor',
            'vendor_code',
            'basis_of_request',
            'details_of_request',
            'invoice_amount',
            'requested_date_of_payment',
            'invoice_date',
            'notes',
            'invoice'
        ]
        widgets = {
            'vendor_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Vendor Name', 
                'style': 'width:100%;'
            }),
            'type_of_vendor': forms.Select(attrs={
                'class': 'form-control', 
                'style': 'width:100%;'
            }),
            'vendor_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Vendor Code', 
                'style': 'width:100%;'
            }),
            'basis_of_request': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Basis of Request', 
                'style': 'width:100%;'
            }),
            'details_of_request': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Details of Request', 
                'rows': 4, 
                'style': 'width:100%;'
            }),
            'invoice_amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Invoice Amount', 
                'style': 'width:100%;'
            }),
            'requested_date_of_payment': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date', 
                'style': 'width:100%;'
            }),
            'invoice_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date', 
                'style': 'width:100%;'
            }),
        }

