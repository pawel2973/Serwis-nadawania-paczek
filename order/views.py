from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.http import request
from django.core.checks import messages
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, request, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import ModelFormMixin, FormMixin

from order.forms import MyForm, ContactForm, AddressForm
from .models import Courier, PackPricing, PalletPricing, EnvelopePricing, Parcel, Order, SenderAddress, Address, \
    RecipientAddress, Profile


class IndexView(generic.FormView):
    template_name = 'order/index.html'
    form_class = MyForm

    def post(self, request, *args, **kwargs):
        form = MyForm(request.POST)  # A form bound to the POST data

        if form.is_valid():
            # TODO : Sprawdz czy wymiary paczki nie przekraczaja maksymalnie dopuszczonych
            # SESSION VARS
            request.session['typ_paczki'] = request.POST['typ_paczki']
            request.session['waga_paczki'] = request.POST['waga_paczki']
            request.session['dlugosc'] = request.POST['dlugosc']
            request.session['szerokosc'] = request.POST['szerokosc']
            request.session['wysokosc'] = request.POST['wysokosc']
            # objs = Parcel.objects.create(length=1, height=1, width=1, weight=1, type=a)
            # print(objs.id)
            return redirect('order:calculate')
        else:
            return render(request, 'order/index.html', {'form': form})


##########################
# FOR testing purposes
g_cname = None
sender_form = None
recipient_form = None
#########################


class CalculateView(generic.ListView):
    template_name = 'order/calculate.html'

    def post(self, request, *args, **kwargs):
        global g_cname
        pack_type = self.request.session.get('typ_paczki')  # get pack type from session
        courier_id = request.session['courier_id'] = request.POST.get('courier')  # get courier_id from button

        if pack_type == "koperta":
            query = list(EnvelopePricing.objects.filter(courier__id=courier_id).values(g_cname))  # query: price from db
            price = query[0].get(g_cname)  # value: price from query
            request.session['price'] = price  # save to session
        elif pack_type == "paczka":
            query = list(PackPricing.objects.filter(courier__id=courier_id).values(g_cname))
            price = query[0].get(g_cname)
            request.session['price'] = price
        elif pack_type == "paleta":
            query = list(PalletPricing.objects.filter(courier__id=courier_id).values(g_cname))
            price = query[0].get(g_cname)
            request.session['price'] = price
        return redirect('order:sender_address')

    def get_queryset(self):
        global g_cname
        ratio = None
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
            g_cname = 'up_to_1'
            return EnvelopePricing.objects.values_list('courier', 'courier__name', 'up_to_1')

        elif type == "paczka":  # Pack Price
            # Set ratio for pack
            if length <= 600 and width <= 500 and height <= 300:  # pack size A
                self.ratio = 1
            elif length <= 3000 and width <= 1500 and height <= 1500:  # pack size B
                self.ratio = 2
            elif length <= 6000 and width <= 3000 and height <= 3000:  # pack size C
                self.ratio = 3
            else:
                pass
                # nie mozna wyslac paczki, obsluga w form albo indexview
                # mozliwy redirect z obsluga bledu

            # Set pack price
            if weight <= 1:
                g_cname = 'up_to_1'
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_1')
            elif weight <= 2:
                g_cname = 'up_to_2'
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_2')
            elif weight <= 5:
                g_cname = 'up_to_5'
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_5')
            elif weight <= 10:
                g_cname = 'up_to_10'
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_10')
            elif weight <= 15:
                g_cname = 'up_to_15'
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_15')
            elif weight <= 20:
                g_cname = 'up_to_20'
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_20')
            elif weight <= 30:
                g_cname = 'up_to_30'
                return PackPricing.objects.values_list('courier', 'courier__name', 'up_to_30')
            else:
                render(request, 'order/index.html')

        elif type == "paleta":  # Pallet Price
            if weight <= 300:
                g_cname = 'up_to_300'
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_300')
            elif weight <= 500:
                g_cname = 'up_to_500'
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_500')
            elif weight <= 800:
                g_cname = 'up_to_800'
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_800')
            elif weight <= 1000:
                g_cname = 'up_to_1000'
                return PalletPricing.objects.values_list('courier', 'courier__name', 'up_to_1000')


class AboutCompanyView(generic.TemplateView):
    template_name = 'order/about.html'


class CourierView(generic.TemplateView):
    template_name = 'order/courier.html'


class SenderAddressView(generic.FormView):
    template_name = 'order/sender_address.html'
    form_class = AddressForm

    def post(self, request, *args, **kwargs):
        global sender_form
        form = AddressForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            sender_form = form
            # sender_obj = form.save(commit=False)
            # sender_obj.save()
            # request.session['sender_obj'] = sender_obj # aborted
            return redirect('order:recipient_address')
        else:
            return render(request, 'order/sender_address.html', {'form': form})


class RecipientAddressView(generic.FormView):
    template_name = 'order/recipient_address.html'
    form_class = AddressForm

    def post(self, request, *args, **kwargs):
        global recipient_form
        form = AddressForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            recipient_form = form
            # request.session['recipient_obj'] = recipient_obj
            return redirect('order:summary')
        else:
            return render(request, 'order/recipient_address.html', {'form': form})


class SummaryView(generic.TemplateView):
    template_name = 'order/summary.html'

    def post(self, request, *args, **kwargs):
        global recipient_form
        global sender_form

        # Creating parcel
        type = self.request.session.get('typ_paczki')
        weight = float(self.request.session.get('waga_paczki'))
        length = float(self.request.session.get('dlugosc'))
        width = float(self.request.session.get('szerokosc'))
        height = float(self.request.session.get('wysokosc'))

        parcel_obj = Parcel.objects.create(length=length, height=height, width=width, weight=weight, type=type)
        parcel_id = parcel_obj.id
        parcel_obj = Parcel.objects.get(id=parcel_id)

        # Creating address
        # sender_obj = request.session.get('sender_obj')
        sender_obj = sender_form.save(commit=False)
        sender_obj.save()
        sender_id = sender_obj.id
        sender_obj = Address.objects.get(id=sender_id)

        # Creating sender address
        sender_address_obj = SenderAddress.objects.create(address=sender_obj)
        sender_address_obj_id = sender_address_obj.id
        sender_address_obj = SenderAddress.objects.get(id=sender_address_obj_id)

        # Creating recipient address
        # recipient_obj = request.session.get('recipient_obj')
        recipient_obj = recipient_form.save(commit=False)
        recipient_obj.save()
        recipient_id = recipient_obj.id
        recipient_obj = Address.objects.get(id=recipient_id)

        recipient_address_obj = RecipientAddress.objects.create(address=recipient_obj)
        recipient_address_obj_id = recipient_address_obj.id
        recipient_address_obj = RecipientAddress.objects.get(id=recipient_address_obj_id)

        print("-----------------------  ADADAD -----------")

        # Creating order
        profile_obj = Profile.objects.get(id=3)
        courier_id = int(request.session.get('courier_id'))
        courier_obj = Courier.objects.get(id=courier_id)

        price = float(request.session.get('price'))
        Order.objects.create(profile=profile_obj, courier=courier_obj, parcel=parcel_obj,
                             recipient=recipient_address_obj,
                             sender=sender_address_obj, status=1, price=price)
        return redirect('order:index')


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
