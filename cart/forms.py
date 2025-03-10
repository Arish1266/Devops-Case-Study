from django import forms
from django.core.validators import MinValueValidator

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES, 
        coerce=int, 
        initial=1,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    override = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=forms.HiddenInput
    )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity