from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Courier, PackPricing, PalletPricing, EnvelopePricing


class IndexView(generic.ListView):
    template_name = 'order/index.html'

    def get_queryset(self):
        return Courier.objects.all()


class AboutCompanyView(generic.TemplateView):
    template_name = 'order/about.html'


class PricingView(generic.ListView):
    template_name = 'order/pricing.html'

    def get_queryset(self):
        return Courier.objects.all()


# class PricingCompanyView(generic.DetailView):
#     model = CourierCompany
#     template_name = 'order/pricing_company.html'


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
