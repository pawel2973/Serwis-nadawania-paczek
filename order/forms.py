from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Address, Opinion


# Validators
def greaterThanZeroValidator(value):
    if value <= 0:
        raise ValidationError(
            _('Wartość musi być większa od 0'),
            params={'value': value},
        )


# SenderAddressView, RecipientAddressView, ProfileAddressCreateView, ProfileAddressUpdateView
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


# FormParcelSize
TYPE = [
    ('koperta', 'Koperta'),
    ('paleta', 'Paleta'),
    ('paczka', 'Paczka'),
]


# IndexView
class FormParcelSize(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    type = forms.ChoiceField(
        choices=TYPE,
        widget=forms.RadioSelect(attrs={'class': ''}),
    )
    weight = forms.FloatField(validators=[greaterThanZeroValidator])
    length = forms.FloatField(validators=[greaterThanZeroValidator])
    width = forms.FloatField(validators=[greaterThanZeroValidator])
    height = forms.FloatField(validators=[greaterThanZeroValidator])


# OpinionCreateView
class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['rating', 'content']
