from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.http import request
from django.core.checks import messages
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, request, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import ModelFormMixin, FormMixin

from order.forms import MyForm, ContactForm
from .models import Courier, PackPricing, PalletPricing, EnvelopePricing


class IndexView(generic.FormView):
    template_name = 'order/index.html'
    form_class = MyForm

    def post(self, request, *args, **kwargs):
        form = MyForm(request.POST)  # A form bound to the POST data

        if form.is_valid():
            # TODO : Sprawdz czy wymiary paczki nie przekraczaja maksymalnie dopuszczonych
            request.session['typ_paczki'] = request.POST['typ_paczki']
            request.session['waga_paczki'] = request.POST['waga_paczki']
            request.session['dlugosc'] = request.POST['dlugosc']
            request.session['szerokosc'] = request.POST['szerokosc']
            request.session['wysokosc'] = request.POST['wysokosc']
            return redirect('order:calculate')
        else:
            return render(request, 'order/index.html', {'form': form})


class CalculateView(generic.ListView):
    template_name = 'order/calculate.html'

    def get_queryset(self):
        # calculate_price()
        ratio = None
        price = None
        type = self.request.session.get('typ_paczki')
        weight = float(self.request.session.get('waga_paczki'))
        length = float(self.request.session.get('dlugosc'))
        width = float(self.request.session.get('szerokosc'))
        height = float(self.request.session.get('wysokosc'))

        if type == "koperta":  # Envelope Price
            # lista = list()
            # print(lista[0])
            # for l in lista:
            #     print(l['up_to_1']*2)
            return EnvelopePricing.objects.values_list('courier', 'courier__name', 'up_to_1')

        elif type == "paczka":  # Pack Price
            # Set ratio for pack
            if length <= 600 and width <= 500 and height <= 300:  # pack size A
                ratio = 1
            elif length <= 3000 and width <= 1500 and height <= 1500:  # pack size B
                ratio = 2
            elif length <= 6000 and width <= 3000 and height <= 3000:  # pack size C
                ratio = 3
            else:
                pass
                # nie mozna wyslac paczki, obsluga w form albo indexview
                # mozliwy redirect z obsluga bledu

            # Set pack price

            if weight <= 1:
                price = 2 * ratio
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_1')
            elif weight <= 2:
                price = 2
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_2')
            elif weight <= 5:
                price = 2
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_5')
            elif weight <= 10:
                price = 2
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_10')
            elif weight <= 15:
                price = 2
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_15')
            elif weight <= 20:
                price = 2
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_20')
            elif weight <= 30:
                price = 2
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_30')
            else:
                render(request, 'order/index.html')

        elif type == "paleta":  # Pallet Price
            if weight <= 300:
                price = 2
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_300')
            elif weight <= 500:
                price = 2
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_500')
            elif weight <= 800:
                price = 2
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_800')
            elif weight <= 1000:
                price = 2
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_1000')


class AboutCompanyView(generic.TemplateView):
    template_name = 'order/about.html'


class CourierView(generic.TemplateView):
    template_name = 'order/courier.html'


class AddressView(generic.TemplateView):
    template_name = 'order/address.html'


class PricingView(generic.ListView):
    template_name = 'order/pricing.html'

    def get_queryset(self):
        return Courier.objects.all()


class PricingCompanyView(generic.TemplateView):
    template_name = 'order/pricing_company.html'

    def get_context_data(self, **kwargs):
        context = super(PricingCompanyView, self).get_context_data(**kwargs)
        context['packpricing'] = PackPricing.objects.get(courier_id=self.kwargs['pk'])
        context['palletpricing'] = PalletPricing.objects.get(courier_id=self.kwargs['pk'])
        context['envelopepricing'] = EnvelopePricing.objects.get(courier_id=self.kwargs['pk'])
        return context


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('order:login')
    template_name = 'registration/signup.html'


'''    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
'''

''' 
def get_queryset(self):
     return Courier.objects.all()

 def get(self, request):
     form = self.form(None)  # we just want use UserForm  # context: None

     # for the form where do you want to go = template_name, and form itself
     return render(request, self.template_name, {'form': form})


 def post(self, request):
     form = ContactForm(request.POST)
     if form.is_valid():
         pass  # does nothing, just trigger the validation
     else:
         form = ContactForm()
     return render(request, 'order/index.html', {'form': form})

'''

'''
def get(self, request, *args, **kwargs):
    # From ProcessFormMixin
    form_class = self.get_form_class()
    #form = self.get_form(form)
    form = self.form(None)

    # From BaseListView
    self.object_list = self.get_queryset()

    context = self.get_context_data(object_list=self.object_list, form=form)
    return self.render_to_response(context)

def post(self, request, *args, **kwargs):
    return self.get(request, *args, **kwargs)
'''
