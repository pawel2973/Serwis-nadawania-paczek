from django import forms
from .models import Address
from django.db import models
from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        #exclude = ['title']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')


TYP_PACZKI = (
    ('koperta', 'Koperta'),
    ('paleta', 'Paleta'),
    ('paczka', 'Paczka'),
)


class MyForm(forms.Form):  # Note that it is not inheriting from forms.ModelForm
    typ_paczki = forms.ChoiceField(
        required=True,
        choices=TYP_PACZKI,
    )
    waga_paczki = forms.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    dlugosc = forms.FloatField(validators=[MinValueValidator(0)])
    szerokosc = forms.FloatField(validators=[MinValueValidator(0)])
    wysokosc = forms.FloatField(validators=[MinValueValidator(0)])


    # def clean(self):
    #     cleaned_data = super(MyForm, self).clean()
    #     typ_paczki = cleaned_data.get('typ_paczki')
    #     waga_paczki = cleaned_data.get('waga_paczki')
    #     dlugosc = cleaned_data.get('dlugosc')
    #     szerokosc = cleaned_data.get('szerokosc')
    #     wysokosc = cleaned_data.get('wysokosc')
    #     if not typ_paczki and not waga_paczki and not dlugosc and not szerokosc and not wysokosc:
    #         raise forms.ValidationError('You have to write something!')
