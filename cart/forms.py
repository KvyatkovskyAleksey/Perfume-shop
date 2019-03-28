from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

class CartAddProductForm(forms.Form):
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, 
									  coerce=int, label='Количество', 
									  )
	quantity.widget.attrs.update({'class':'form-control',
								  })
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

	
