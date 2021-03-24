from django import forms

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range (1,20)]

class cart_add_form(forms.Form):
    quantity = forms.TypedChoiceField(coerce=int, choices=(PRODUCT_QUANTITY_CHOICES))
    override = forms.BooleanField(required=False, initial=False,widget=forms.HiddenInput)
