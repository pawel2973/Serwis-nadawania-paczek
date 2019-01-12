from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.http import request
from django.core.checks import messages
from django.db import IntegrityError
from django.db.models import Count, Avg
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, request, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from django.views import generic

from .forms import FormParcelSize, AddressForm, OpinionForm
from .models import Courier, PackPricing, PalletPricing, EnvelopePricing, Parcel, Order, SenderAddress, Address, \
    RecipientAddress, Profile, Opinion, GiftAddress, Gift, OrderGift
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.template.defaulttags import register
from .fusioncharts import FusionCharts


# Views of the package ordering process
# ---------------------------------------------------------------------------------------------------------------------
class IndexView(generic.FormView):
    template_name = 'order/index.html'
    form_class = FormParcelSize

    def choose_pricing_col_and_ratio(self, parcel_type, weight, length, width, height):
        col_name_pricing = None
        if parcel_type == "koperta":  # Envelope Price
            col_name_pricing = 'up_to_1'
        elif parcel_type == "paczka":  # Pack Price
            # Set ratio for pack
            if length <= 60 and width <= 50 and height <= 30:  # pack size A
                self.request.session['ratio'] = 1.0
            elif length <= 80 and width <= 70 and height <= 50:  # pack size B
                self.request.session['ratio'] = 2.0
            elif length <= 100 and width <= 90 and height <= 70:  # pack size C
                self.request.session['ratio'] = 3.0
            # Set pack price
            if weight <= 1:
                col_name_pricing = 'up_to_1'
            elif weight <= 2:
                col_name_pricing = 'up_to_2'
            elif weight <= 5:
                col_name_pricing = 'up_to_5'
            elif weight <= 10:
                col_name_pricing = 'up_to_10'
            elif weight <= 15:
                col_name_pricing = 'up_to_15'
            elif weight <= 20:
                col_name_pricing = 'up_to_20'
            elif weight <= 30:
                col_name_pricing = 'up_to_30'

        elif parcel_type == "paleta":  # Pallet Price
            if weight <= 300:
                col_name_pricing = 'up_to_300'
            elif weight <= 500:
                col_name_pricing = 'up_to_500'
            elif weight <= 800:
                col_name_pricing = 'up_to_800'
            elif weight <= 1000:
                col_name_pricing = 'up_to_1000'

        return col_name_pricing

    def post(self, request, *args, **kwargs):
        form = FormParcelSize(request.POST)  # A form bound to the POST data

        if form.is_valid():
            # SESSION VARS
            parcel_type = request.POST['type']
            weight = float(request.POST['weight'])
            length = float(request.POST['length'])
            width = float(request.POST['width'])
            height = float(request.POST['height'])

            if parcel_type == "koperta":
                # envelope size: .5kg x 35cm x 25cm x 5cm
                if length > 35 or width > 25 or height > 5 or weight > 1:
                    context = {'form': form, 'error_parcel': 'Niepoprawne wymiary dla koperty!'}
                    return render(request, 'order/index.html', context)
            elif parcel_type == "paczka":
                # pack size: 30kg x 100cm x 90cm x 70cm
                if length > 100 or width > 90 or height > 70 or weight > 30:  # pack size C
                    context = {'form': form, 'error_parcel': 'Niepoprawne wymiary dla paczki!'}
                    return render(request, 'order/index.html', context)
            elif parcel_type == "paleta":
                # pallet size: 1000kg x 200cm x 140cm x 200cm
                if length > 200 or width > 140 or height > 200 or weight > 1000:  # pack size C
                    context = {'form': form, 'error_parcel': 'Niepoprawne wymiary dla palety!'}
                    return render(request, 'order/index.html', context)

            request.session['col_name_pricing'] = self.choose_pricing_col_and_ratio(parcel_type, weight, length, width,
                                                                                    height)
            request.session['type'] = parcel_type
            request.session['weight'] = weight
            request.session['length'] = length
            request.session['width'] = width
            request.session['height'] = height
            if request.session.get('courier_id') is not None:
                del request.session['courier_id']
            return redirect('order:choose_courier')
        else:
            return render(request, 'order/index.html', {'form': form})


class ChooseCourierView(generic.ListView):
    template_name = 'order/choose-courier.html'

    def dispatch(self, request, *args, **kwargs):
        parcel_type = self.request.session.get('type')

        if parcel_type is None:
            return redirect('order:index')
        else:
            return super(ChooseCourierView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        courier_id = request.session['courier_id'] = request.POST.get('courier')  # get courier_id from button
        if courier_id is None:
            request.session['error_courier'] = "Nie wybrałeś kuriera!"
            return redirect('order:choose_courier')
        if request.session.get('error_courier') is not None:
            del request.session['error_courier']

        col_name_pricing = request.session.get('col_name_pricing')
        parcel_type = request.session.get('type')  # get pack type from session
        ratio = request.session.get('ratio')

        if parcel_type == "koperta":
            query = list(
                EnvelopePricing.objects.filter(courier__id=courier_id).values(col_name_pricing))  # query: price from db
            price = query[0].get(col_name_pricing)  # value: price from query
            request.session['price'] = price  # save to session
        elif parcel_type == "paczka":
            query = list(PackPricing.objects.filter(courier__id=courier_id).values(col_name_pricing))
            price = query[0].get(col_name_pricing) * ratio
            request.session['price'] = price
        elif parcel_type == "paleta":
            query = list(PalletPricing.objects.filter(courier__id=courier_id).values(col_name_pricing))
            price = query[0].get(col_name_pricing)
            request.session['price'] = price
        return redirect('order:sender_address')

    def get_queryset(self):
        col_name_pricing = self.request.session.get('col_name_pricing')
        parcel_type = self.request.session.get('type')
        ratio = self.request.session.get('ratio')

        if parcel_type == 'koperta':
            return EnvelopePricing.objects.values_list('courier', 'courier__name', col_name_pricing)
        elif parcel_type == 'paczka':
            pack_price_col = list(PackPricing.objects.values_list('courier', 'courier__name', col_name_pricing))
            real_pack_price = list()

            for x in pack_price_col:
                price = round(x[2] * ratio, 2)
                real_pack_price.append(tuple([x[0], x[1], price]))
            return real_pack_price
        elif parcel_type == 'paleta':
            return PalletPricing.objects.values_list('courier', 'courier__name', col_name_pricing)


class SenderAddressView(generic.FormView):
    template_name = 'order/sender_address.html'
    form_class = AddressForm

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('courier_id') is None:
            return redirect('order:index')
        else:
            return super(SenderAddressView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            request.session['sender_form'] = form.cleaned_data  # thanks to pickle serializer
            return redirect('order:recipient_address')
        else:
            return render(request, 'order/sender_address.html', {'form': form})


class RecipientAddressView(generic.FormView):
    template_name = 'order/recipient_address.html'
    form_class = AddressForm

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('sender_form') is None:
            return redirect('order:index')
        else:
            return super(RecipientAddressView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            request.session['recipient_form'] = form.cleaned_data
            return redirect('order:summary')
        else:
            return render(request, 'order/recipient_address.html', {'form': form})


class SummaryView(generic.TemplateView):
    template_name = 'order/summary.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.session.get('recipient_form'))
        print(request.session.get('courier_id'))
        if request.session.get('recipient_form') is None or request.session.get('courier_id') is None:
            return redirect('order:index')
        else:
            return super(SummaryView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SummaryView, self).get_context_data(**kwargs)
        # parcel info
        context['type'] = self.request.session.get('type')
        context['weight'] = float(self.request.session.get('weight'))
        context['length'] = float(self.request.session.get('length'))
        context['width'] = float(self.request.session.get('width'))
        context['height'] = float(self.request.session.get('height'))
        context['price'] = float(self.request.session.get('price'))

        # courier info
        courier_id = int(self.request.session.get('courier_id'))
        context['courier'] = Courier.objects.get(id=courier_id)

        # sender info
        sender_form = self.request.session.get('sender_form')
        context['sender_obj'] = Address(**sender_form)

        # recipient info
        recipient_form = self.request.session.get('recipient_form')
        context['recipient_obj'] = Address(**recipient_form)

        # add premium points
        context['premium_points'] = int(self.request.session.get('price'))
        return context

    def post(self, request, *args, **kwargs):
        # Creating parcel
        parcel_type = self.request.session.get('type')
        weight = float(self.request.session.get('weight'))
        length = float(self.request.session.get('length'))
        width = float(self.request.session.get('width'))
        height = float(self.request.session.get('height'))

        # Creating Parcel db
        parcel_obj = Parcel.objects.create(length=length, height=height, width=width, weight=weight, type=parcel_type)
        parcel_id = parcel_obj.id
        parcel_obj = Parcel.objects.get(id=parcel_id)

        # Creating Address for sender db
        sender_form = request.session.get('sender_form')
        sender_obj = Address(
            **sender_form)  # Unwrap the dictionary, making its keys and values act like named arguments

        # TODO clean the data before sending form !
        # sender_obj = sender_obj.save(commit=False) # now impossible

        # Save Address form
        sender_obj.save()
        sender_id = sender_obj.id
        sender_obj = Address.objects.get(id=sender_id)

        # Creating SenderAddress db
        sender_address_obj = SenderAddress.objects.create(address=sender_obj)
        sender_address_obj_id = sender_address_obj.id
        sender_address_obj = SenderAddress.objects.get(id=sender_address_obj_id)

        # Creating Address for recipient db
        recipient_form = request.session.get('recipient_form')
        recipient_obj = Address(**recipient_form)

        # Save Address form
        recipient_obj.save()
        recipient_id = recipient_obj.id
        recipient_obj = Address.objects.get(id=recipient_id)

        # Creating RecipientAddress db
        recipient_address_obj = RecipientAddress.objects.create(address=recipient_obj)
        recipient_address_obj_id = recipient_address_obj.id
        recipient_address_obj = RecipientAddress.objects.get(id=recipient_address_obj_id)

        # Get profile id
        get_profile = Profile.objects.get(user_id=self.request.user.id)

        # Creating order db
        profile_obj = Profile.objects.get(id=get_profile.id)
        courier_id = int(request.session.get('courier_id'))
        courier_obj = Courier.objects.get(id=courier_id)

        price = float(request.session.get('price'))
        Order.objects.create(profile=profile_obj, courier=courier_obj, parcel=parcel_obj,
                             recipient=recipient_address_obj,
                             sender=sender_address_obj, price=price)

        # Add premium points
        profile_obj.premium_points += int(price)
        profile_obj.save()

        # DEL session vars
        del request.session['type']
        del request.session['weight']
        del request.session['length']
        del request.session['width']
        del request.session['height']
        del request.session['courier_id']
        del request.session['price']
        del request.session['sender_form']
        del request.session['recipient_form']
        if request.session.get('ratio') is not None:
            del request.session['ratio']

        request.session['order_success'] = "Dziękujemy za złożenie zamówienia. " \
                                           "Szczegóły oraz status konkretnego zamówienia " \
                                           "możesz sprawdzić w liście poniżej."
        return redirect('order:orders')


# Pricing Views
# ---------------------------------------------------------------------------------------------------------------------
class PricingView(generic.ListView):
    template_name = 'order/pricing.html'

    def get_queryset(self):
        return Courier.objects.all()


class PricingCompanyView(generic.TemplateView):
    template_name = 'order/pricing_company.html'

    def get_context_data(self, **kwargs):
        context = super(PricingCompanyView, self).get_context_data(**kwargs)
        try:
            context['packpricing'] = PackPricing.objects.get(courier_id=self.kwargs['pk'])
            context['palletpricing'] = PalletPricing.objects.get(courier_id=self.kwargs['pk'])
            context['envelopepricing'] = EnvelopePricing.objects.get(courier_id=self.kwargs['pk'])
        except:
            context['error'] = True

        context['opinion'] = Opinion.objects.filter(order__courier_id=self.kwargs['pk'])
        if not context['opinion']:
            context['no_opinions'] = True

        return context


# About Company View
# ---------------------------------------------------------------------------------------------------------------------
class AboutCompanyView(generic.TemplateView):
    template_name = 'order/about.html'


# User Profile Views
# ---------------------------------------------------------------------------------------------------------------------
class ProfileView(generic.TemplateView):
    template_name = 'order/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(ProfileView, self).dispatch(request, *args, **kwargs)
        return redirect('order:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_profile = Profile.objects.get(user_id=self.request.user.id)
        get_gift_orders = OrderGift.objects.all().filter(profile=get_profile).order_by('-id')

        if get_profile.address is not None:
            profile_address = get_profile.address.__dict__
            context['profile_address'] = profile_address
        if get_gift_orders is not None:
            context['gift_orders'] = get_gift_orders
        context['profile'] = get_profile
        get_gifts = Gift.objects.all().order_by('-premium_points')
        context['gifts'] = get_gifts
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        # Get gift premium points
        gift_id = request.POST.get('submit')
        gift_obj = Gift.objects.get(pk=gift_id)
        gift_premium_points = gift_obj.premium_points

        # Get profile premium points
        profile_obj = Profile.objects.get(user_id=self.request.user.id)
        profile_premium_points = profile_obj.premium_points

        if profile_obj.address is None:
            context['gift_order_error'] = "Nie podałeś adresu w swoim profilu!"
            return super(ProfileView, self).render_to_response(context)
        elif gift_premium_points > profile_premium_points:
            context['gift_order_error'] = "Nie posiadasz wystarczającej ilości punktów premium!"
            return super(ProfileView, self).render_to_response(context)
        else:
            # Remove some premium points
            profile_obj.premium_points -= gift_premium_points
            profile_obj.save()
            # Create gift order
            profile_address_obj = profile_obj.address
            gift_address_obj = GiftAddress.objects.create(name=profile_address_obj.name,
                                                          surname=profile_address_obj.surname,
                                                          company_name=profile_address_obj.company_name,
                                                          zip_code=profile_address_obj.zip_code,
                                                          city=profile_address_obj.city,
                                                          street=profile_address_obj.street,
                                                          house_number=profile_address_obj.house_number,
                                                          apartment_number=profile_address_obj.apartment_number,
                                                          telephone_number=profile_address_obj.telephone_number,
                                                          email_address=profile_address_obj.email_address,
                                                          nip=profile_address_obj.nip)
            OrderGift.objects.create(profile=profile_obj, recipient=gift_address_obj, gift=gift_obj)
            context['profile'] = profile_obj
            context['gift_order_success'] = "Nagroda została zamówiona pomyślnie. Oczekuj niespodzianki wkrótce."
            return super(ProfileView, self).render_to_response(context)


class ProfileAddressCreateView(generic.FormView):
    template_name = 'order/create_profile_address.html'
    form_class = AddressForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            get_profile = Profile.objects.get(user_id=self.request.user.id)
            if get_profile.address_id is None:
                return super(ProfileAddressCreateView, self).dispatch(request, *args, **kwargs)
        return redirect('order:profile')

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            object = form.save()
            Profile.objects.filter(user_id=self.request.user.id).update(address=object.id)
            return redirect('order:profile')
        else:
            return render(request, self.template_name, {'form': form})


class ProfileAddressUpdateView(generic.UpdateView):
    template_name = 'order/create_profile_address.html'
    model = Address
    form_class = AddressForm
    success_url = reverse_lazy('order:profile')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            get_profile = Profile.objects.get(user_id=self.request.user.id)
            obj = self.get_object()
            # Check address ownership
            if obj.id != get_profile.address_id:
                return redirect('order:profile')
            return super(ProfileAddressUpdateView, self).dispatch(request, *args, **kwargs)
        return redirect('order:index')


class ProfileAddressDeleteView(generic.DeleteView):
    model = Address
    success_url = reverse_lazy('order:profile')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            get_profile = Profile.objects.get(user_id=self.request.user.id)
            obj = self.get_object()
            # Check address ownership
            if obj.id != get_profile.address_id:
                return redirect('order:profile')
            return super(ProfileAddressDeleteView, self).dispatch(request, *args, **kwargs)
        return redirect('order:index')


# User Orders Views
# ---------------------------------------------------------------------------------------------------------------------

class OrdersView(generic.TemplateView):
    template_name = 'order/user_orders.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(OrdersView, self).dispatch(request, *args, **kwargs)
        return redirect('order:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_profile = Profile.objects.get(user_id=self.request.user.id)
        get_order_list = Order.objects.filter(profile_id=get_profile.id).order_by('-id')
        # print(get_order_list)
        context['order_list'] = get_order_list
        if self.request.session.get('order_success') is not None:
            context['order_success'] = self.request.session.get('order_success')
            del self.request.session['order_success']
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        order_id = request.POST.get('submit')
        order_obj = Order.objects.get(pk=order_id)
        if order_obj.status != 0:
            context['cancel_error'] = "Nie możesz anulować zamówienia o nr: " + str(order_id)
            return super(OrdersView, self).render_to_response(context)
        else:
            points_to_remove = int(order_obj.price)
            get_profile = Profile.objects.get(user_id=self.request.user.id)
            profile_obj = Profile.objects.get(id=get_profile.id)
            profile_obj.premium_points -= points_to_remove
            if profile_obj.premium_points < 0:
                context['cancel_error'] = "Nie możesz anulować zamówienia o nr: " + str(
                    order_id) + " ponieważ wykorzystałeś swoje punkty premium!"
            else:
                profile_obj.save()
                order_obj.status = 3
                order_obj.save()
                context['cancel_success'] = "Pomyślnie anulowano zamówienie o nr: " + str(order_id)
            return super(OrdersView, self).render_to_response(context)


# Opinion View
# ---------------------------------------------------------------------------------------------------------------------
class OpinionCreateView(generic.FormView):
    template_name = 'order/opinion_create.html'
    form_class = OpinionForm

    def dispatch(self, request, *args, **kwargs):
        order_id = request.GET.get('order_id')
        if self.request.user.is_authenticated:
            if order_id is not None:
                try:
                    int(order_id)
                except ValueError:
                    return redirect('order:index')
                if Order.objects.get(pk=order_id).profile.user == self.request.user:
                    return super(OpinionCreateView, self).dispatch(request, *args, **kwargs)
        return redirect('order:index')

    # def get(self, request, *args, **kwargs):
    #     request.session['order_id'] = request.GET.get('order_id')
    #     return super(OpinionCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = OpinionForm(request.POST)  # A form bound to the POST data
        if form.is_valid():
            my_data = form.cleaned_data
            order_obj = Order.objects.get(pk=request.GET.get('order_id'))
            try:
                Opinion.objects.create(order=order_obj, content=my_data['content'],
                                       rating=my_data['rating'])
                # del request.session['order_id']
                return redirect('order:pricing_company', pk=order_obj.courier_id)
            except IntegrityError:
                return render(request, 'order/opinion_create.html',
                              {'form': form, 'error_unique': 'To zamowienie juz ma dodana opinie'})
            # return redirect('order:pricing_company', pk=order_obj.courier_id)
        else:
            return render(request, 'order/opinion_create.html', {'form': form})


# Courier Ranking Views
# ---------------------------------------------------------------------------------------------------------------------
class CourierRankingView(generic.TemplateView):
    template_name = 'order/courier_ranking.html'

    def get_context_data(self, **kwargs):
        context = super(CourierRankingView, self).get_context_data(**kwargs)
        context['top'] = list(
            Order.objects.all().values('courier__name').annotate(total=Count('courier')).order_by('-total')[:5])
        all_couriers = Order.objects.all().count()
        for i in range(len(context['top'])):
            context['top'][i]['total'] /= all_couriers
            context['top'][i]['total'] *= 100
            context['top'][i]['total'] = round(context['top'][i]['total'], 2)
        context['top'].append(
            {'courier__name': 'Inne firmy', 'total': round(100 - sum(list(d['total'] for d in context['top'])), 2)})
        return context


class ChartsView(generic.TemplateView):
    template_name = 'order/charts.html'

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)

        # CHART: COURIER -> PARCELS
        # -----------------------------------------------------------
        dataSource = {}
        dataSource['chart'] = {
            "caption": "Liczba zamówionych przesyłek",
            "theme": "fusion"
        }

        # Convert the data in the `actualData` array into a format that can be consumed by FusionCharts.
        # The data for the chart should be in an array wherein each element of the array is a JSON object
        # having the `label` and `value` as keys.
        dataSource['data'] = []

        courier_order_list = Order.objects.all().values('courier__name').annotate(total=Count('courier')).order_by(
            '-total')

        for idx, dict in enumerate(courier_order_list):
            data = {}
            data['label'] = dict['courier__name']
            data['value'] = dict['total']
            dataSource['data'].append(data)

        # FusionCharts class constructor
        courier_parcels_bar3D = FusionCharts("bar3d", "ex1", "100%", "400", "chart-1", "json", dataSource)

        context['courier_parcels_bar3D'] = courier_parcels_bar3D.render()

        return context


# Register & Login Views
# ---------------------------------------------------------------------------------------------------------------------
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('order:login')
    template_name = 'registration/signup.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('order:index')
        return super().dispatch(*args, **kwargs)


class LogoutView(generic.RedirectView):
    # Provides users the ability to logout
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


@register.filter
def get_range(value):
    return range(value)
