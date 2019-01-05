from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, RegexValidator, \
    MaxValueValidator  # !!! READ DOC !!!
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.datetime_safe import datetime


def name_validator():
    return RegexValidator(
        r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$",
        'To pole moze skladac sie tylko z liter.')


def zip_code_validator():
    return RegexValidator(r'\d{2}-\d{3}', 'Podaj poprawny adres pocztowy NN-NNN')


class Address(models.Model):
    name = models.CharField(max_length=90, validators=[name_validator()])
    surname = models.CharField(max_length=90, validators=[name_validator()])
    company_name = models.CharField(max_length=500, blank=True)  # isOptional
    zip_code = models.CharField(max_length=6, validators=[zip_code_validator()])  # Poland only
    city = models.CharField(max_length=350, validators=[name_validator()])
    street = models.CharField(max_length=350)
    house_number = models.IntegerField(validators=[MinValueValidator(0)])
    apartment_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])  # isOptional
    telephone_number = models.CharField(max_length=20, validators=[MinLengthValidator(9)])  # !!! READ DOC !!!
    email_address = models.EmailField(max_length=250)
    nip = models.CharField(null=True, blank=True, max_length=10,
                           validators=[MinLengthValidator(10), MaxLengthValidator(10)])  # !!! READ DOC !!!

    def __str__(self):
        show_nip = self.nip
        show_apartment_number = self.apartment_number
        show_company = self.company_name

        if show_nip is None:
            show_nip = ""
        else:
            show_nip = " - nip: " + show_nip
        if show_apartment_number is None:
            show_apartment_number = ""
        else:
            show_apartment_number = "/" + str(show_apartment_number)
        if show_company is None:
            show_company = ""

        return str(self.name) + " " + str(self.surname) + " | " + str(
            self.zip_code) + " " + str(self.city) + " ul. " + str(self.street) + " " + str(
            self.house_number) + str(
            show_apartment_number) + " | tel: " + str(self.telephone_number) + " | " + str(
            self.email_address) + " | " + str(show_company) + str(show_nip)


class Profile(models.Model):
    # default: username, password, email, groups
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # user_id
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)  # address_id
    premium_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # przy tworzeniu użytkownika user, tworzony jest automatycznie profil
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.__str__()


class RecipientAddress(models.Model):
    address = models.OneToOneField(Address, on_delete=models.PROTECT, null=True)  # address_id

    def __str__(self):
        return self.address.name + " " + self.address.surname


class SenderAddress(models.Model):
    address = models.OneToOneField(Address, on_delete=models.PROTECT, null=True)  # address_id

    def __str__(self):
        return self.address.name + " " + self.address.surname


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

    def __str__(self):
        return self.courier.__str__()


class PalletPricing(models.Model):
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE, null=True)  # courier_id
    up_to_300 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_500 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_800 = models.FloatField(validators=[MinValueValidator(0)])
    up_to_1000 = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.courier.__str__()


class EnvelopePricing(models.Model):
    courier = models.OneToOneField(Courier, on_delete=models.CASCADE, null=True)  # courier_id
    up_to_1 = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.courier.__str__()


class Parcel(models.Model):
    length = models.FloatField(validators=[MinValueValidator(0)])
    width = models.FloatField(validators=[MinValueValidator(0)])
    height = models.FloatField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    type = models.CharField(max_length=8)  # enum ???
    content = models.TextField(max_length=3000, blank=True)  # dodac blank

    def __str__(self):
        return self.type + " / " + str(self.weight) + " kg / " + str(self.length) + " x " + str(
            self.weight) + " x " + str(self.height) + " cm "


PACK_STATUS = (
    (0, 'Przygotowane do wysyłki'),
    (1, 'W drodze'),
    (2, 'Dostarczono'),
    (3, 'Anulowano'),
)


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, null=False)  # profile_id != user_id
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=False)  # courier_id
    parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE, null=False)  # parcel_id
    recipient = models.ForeignKey(RecipientAddress, on_delete=models.CASCADE, null=False)  # recipient_id
    sender = models.ForeignKey(SenderAddress, on_delete=models.CASCADE, null=False)  # sender_id
    status = models.IntegerField(
        default=0,
        choices=PACK_STATUS,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )
    price = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return "#" + str(self.id) + " | " + str(self.courier) + " | " + str(
            self.parcel) + " | status: " + str(PACK_STATUS[self.status][1]) + " | cena: " + str(self.price) + " zł"

class Opinion(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False)
    date = models.DateField(default=datetime.now)
    content = models.TextField(max_length=3000)
    rating = models.IntegerField(choices=list(zip(range(1, 11), range(1, 11))))

    def __str__(self):
        return "Ocena: " + str(self.rating) + " | " + str(self.order.courier) + "  | Dnia: " + str(self.date)