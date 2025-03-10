from django import forms
from django.core.validators import RegexValidator
from .models import Order, Coupon

class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    shipping_first_name = forms.CharField(
        label='First Name', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_last_name = forms.CharField(
        label='Last Name', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_address = forms.CharField(
        label='Address', 
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_city = forms.CharField(
        label='City', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_state = forms.CharField(
        label='State/Province', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_zip_code = forms.CharField(
        label='Zip/Postal Code', 
        max_length=20,
        validators=[
            RegexValidator(
                r'^\d{5}(-\d{4})?$', 
                'Enter a valid zip code (e.g. 12345 or 12345-6789)'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_country = forms.CharField(
        label='Country', 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    payment_method = forms.ChoiceField(
        label='Payment Method',
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Order
        fields = [
            'shipping_first_name', 'shipping_last_name', 
            'shipping_address', 'shipping_city', 
            'shipping_state', 'shipping_zip_code', 
            'shipping_country', 'payment_method'
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation logic here
        return cleaned_data

class CouponForm(forms.Form):
    code = forms.CharField(
        label='Coupon Code', 
        max_length=50, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter coupon code'
        })
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            if not coupon.is_valid():
                raise forms.ValidationError("This coupon is no longer valid.")
        except Coupon.DoesNotExist:
            raise forms.ValidationError("Invalid coupon code.")
        return code