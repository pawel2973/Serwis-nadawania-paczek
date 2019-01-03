from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Address
from django.db import models
from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator


def greaterThanZeroValidator(value):
    if value <= 0:
        raise ValidationError(
            _('Wartość musi być większa od 0'),
            params={'value': value},
        )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        # exclude = ['title']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')


TYPE = [
    ('koperta', 'Koperta'),
    ('paleta', 'Paleta'),
    ('paczka', 'Paczka'),
]


class FormParcelSize(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    type = forms.ChoiceField(
        choices=TYPE,
        widget=forms.RadioSelect(attrs={'class': ''}),
    )
    weight = forms.FloatField(validators=[greaterThanZeroValidator])
    length = forms.FloatField(validators=[greaterThanZeroValidator])
    width = forms.FloatField(validators=[greaterThanZeroValidator])
    height = forms.FloatField(validators=[greaterThanZeroValidator])

# class EnvelopeForm(forms.Form):
#     pack_type = forms.CharField(default="koperta", hidden=True)
#     weight = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(0.5)])
#     length = forms.FloatField(disabled=True)
#     width = forms.FloatField(disabled=True)
#     height = forms.FloatField(disabled=True)


# def clean(self):
#     cleaned_data = super(MyForm, self).clean()
#     typ_paczki = cleaned_data.get('typ_paczki')
#     waga_paczki = cleaned_data.get('waga_paczki')
#     dlugosc = cleaned_data.get('dlugosc')
#     szerokosc = cleaned_data.get('szerokosc')
#     wysokosc = cleaned_data.get('wysokosc')
#     if not typ_paczki and not waga_paczki and not dlugosc and not szerokosc and not wysokosc:
#         raise forms.ValidationError('You have to write something!')
