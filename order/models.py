from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator  # !!! READ DOC !!!
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.datetime_safe import datetime



class Address(models.Model):
    name = models.CharField(max_length=90)
    surname = models.CharField(max_length=90)
    company_name = models.CharField(max_length=500, blank=True)  # isOptional
    zip_code = models.CharField(max_length=6)  # Poland only
    city = models.CharField(max_length=350)
    street = models.CharField(max_length=350)
    house_number = models.CharField(max_length=7)
    apartment_number = models.IntegerField(null=True, blank=True, validators=[MaxLengthValidator(7)])  # isOptional
    telephone_number = models.CharField(max_length=20, validators=[MinLengthValidator(9)])  # !!! READ DOC !!!
    email_address = models.EmailField(max_length=250)
    nip = models.CharField(null=True, blank=True, max_length=10, validators=[MinLengthValidator(10), MaxLengthValidator(10)])  # !!! READ DOC !!!


class Profile(models.Model):
    # default: username, password, email, groups
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # user_id
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)  # address_id
    premium_points = models.IntegerField(default=0, editable=False, validators=[MinValueValidator(0)])

    # przy tworzeniu użytkownika user, tworzony jest automatycznie profil
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # def get_absolute_url(self):
    #     return reverse('order:index', kwargs={'pk': self.pk})


class RecipientAddress(models.Model):
    address = models.OneToOneField(Address, on_delete=models.PROTECT, null=True)  # address_id


class SenderAddress(models.Model):
    address = models.OneToOneField(Address, on_delete=models.PROTECT, null=True)  # address_id


class Courier(models.Model):
    # add ranking
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class PackPricing(models.Model):
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE, null=True)  # courier_id
    up_to_1 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_2 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_5 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_10 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_15 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_20 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_30 = models.FloatField(validators=[MinValueValidator(0)])


class PalletPricing(models.Model):
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE, null=True)  # courier_id
    up_to_300 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_500 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_800 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_1000 = models.FloatField(validators=[MinValueValidator(0)])


class EnvelopePricing(models.Model):
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE, null=True)  # courier_id
    up_to_1 = models.FloatField(validators=[MinValueValidator(0)])


class Parcel(models.Model):
    length = models.FloatField(validators=[MinValueValidator(0)])
    height = models.FloatField(validators=[MinValueValidator(0)])
    width = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    type = models.CharField(max_length=8)  # enum ???
    content = models.TextField(max_length=3000)


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=False)  # profile_id
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE, null=False)  # courier_id
    parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE, null=False)  # parcel_id
    recipient = models.ForeignKey(RecipientAddress, on_delete=models.CASCADE, null=False)  # recipient_id
    sender = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, null=False)  # sender_id
    status = models.IntegerField(validators=[MinLengthValidator(1), MaxLengthValidator(1), MinValueValidator(0)])
    price = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateField(default=datetime.now)

