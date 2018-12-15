from django.contrib import admin
from .models import Courier, Order, Parcel, SenderAddress, RecipientAddress, Profile, Address, EnvelopePricing, \
    PackPricing, PalletPricing

admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(RecipientAddress)
admin.site.register(SenderAddress)
admin.site.register(Courier)
admin.site.register(PackPricing)
admin.site.register(PalletPricing)
admin.site.register(EnvelopePricing)
admin.site.register(Parcel)
admin.site.register(Order)
