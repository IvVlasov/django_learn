from django import forms


class OrderCreationForm(forms.Form):
    city = forms.CharField(
        max_length=32, widget=forms.TextInput(
            attrs={'class': 'checkout_input'}
        )
    )
    street = forms.CharField(
        max_length=32, widget=forms.TextInput(
            attrs={'class': 'checkout_input'}
        )
    )
    street_num = forms.CharField(
        max_length=32, widget=forms.TextInput(
            attrs={'class': 'checkout_input'}
        )
    )
    appart_num = forms.CharField(
        max_length=32, widget=forms.TextInput(
            attrs={'class': 'checkout_input'}
        )
    )
