from django.utils import timezone

from django.db import models

from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CarModel(models.Model):
    manufacturer_model_name = models.CharField(
        max_length=15,
        verbose_name="Model",
        help_text="Enter a car manufacturer model name e.g. Mustang"
    )
    manufacturer_name_and_logo = models.ForeignKey(
        'CarManufacturerAndLogo',
        verbose_name="Car Make and Logo",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['manufacturer_name_and_logo', 'manufacturer_model_name']
        unique_together = (
            ('manufacturer_name_and_logo',
            'manufacturer_model_name'),
        )

    def __str__(self):
        return '{} {}'.format(
            self.manufacturer_name_and_logo,
            self.manufacturer_model_name
        )


class CarManufacturerAndLogo(models.Model):
    manufacturer_logo = models.ImageField(
        upload_to='images',
        verbose_name="Car Logo"
    )
    manufacturer_logo_name = models.CharField(
        max_length=15,
        verbose_name="Make",
        help_text="Enter a car manufacturer name e.g. Ford",
    )

    class Meta:
        verbose_name_plural = "Car Make and Logo"
        unique_together = (
            ('manufacturer_logo_name'),
        )

    def __str__(self):
        return '{}'.format(self.manufacturer_logo_name)


class Car(models.Model):
    car_make_and_model = models.ForeignKey(
        CarModel,
        verbose_name="Make and Model"
    )
    car_body = models.ForeignKey('BodyType')
    car_type = models.ForeignKey('CarType')
    num_of_doors = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        default=4,
        verbose_name="Doors"
    )
    passangers = models.DecimalField(max_digits=1, decimal_places=0, default=5)
    car_image = models.ImageField(upload_to='images')

    class Meta:
        ordering = [
            "car_make_and_model__manufacturer_name_and_logo__manufacturer_logo_name",
            "car_make_and_model__manufacturer_model_name"]
        unique_together = (
            ('car_make_and_model',
            'car_body',
            'car_type',
            'num_of_doors',
            'passangers'),
        )

    def __str__(self):
            return '{} {} {} Doors'.format(
                self.car_make_and_model,
                self.car_body,
                self.num_of_doors
            )

    def get_car_body(self):
        return self.car_body.get_body_type_display()
    get_car_body.short_description = 'Car Body'

    def get_car_type(self):
        return self.car_type.get_car_type_display()
    get_car_type.short_description = 'Car Type'

    def get_absolute_url(self):
        return reverse('car-detail',args=[str(self.id)])


class BodyType(models.Model):
    BODY_CHOICE = (
        ('sed', 'Sedan'),
        ('hat', 'Hatchback'),
        ('est', 'Estate'),
        ('mpv', 'MPV'),
        ('cop', 'Coupe'),
        ('con', 'Convertible'),
        ('suv', 'SUV'),
        ('pic', 'Pickup'),
        ('cab', 'Cabriolet'),
        ('com', 'Commercial'),
        ('van', 'Van'),
        ('oth', 'Other'),
    )
    body_type = models.CharField(
        max_length=3,
        choices=BODY_CHOICE,
        default='sal',
        verbose_name='Body',
        help_text='Choose car body type'
    )

    class Meta:
        unique_together = (('body_type'),)

    def __str__(self):
        return '{}'.format(self.get_body_type_display())


class CarType(models.Model):

    Mini = 1
    Economy = 2
    Compact = 3
    Intermediate = 4
    Carrier = 5
    Premium = 6
    Sport = 7
    Other = 8

    TYPE_CHOICE = (
        (Mini, 'Mini'),
        (Economy, 'Economy'),
        (Compact, 'Compact'),
        (Intermediate, 'Intermediate'),
        (Carrier, 'Carrier'),
        (Premium, 'Premium'),
        (Sport, 'Sport'),
        (Other, 'Other'),
    )

    car_type = models.PositiveIntegerField(
        choices=TYPE_CHOICE,
        default=3,
        help_text='Choose car type'
    )

    class Meta:
        unique_together = (('car_type'),)
        ordering = ["car_type"]

    def __str__(self):
        return '{}'.format(self.get_car_type_display())


class CarSpecs(models.Model):
    specification = models.CharField(
        max_length=25,
        help_text="Enter a car specs (e.g. Audio System, Sunroof, Airbags)"
    )

    class Meta:
        unique_together = (('specification'),)

    def __str__(self):
        return '{}'.format(self.specification)


class CarEngineSize(models.Model):
    engine_size = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=1.0
    )

    class Meta:
        unique_together = (('engine_size'),)

    def __str__(self):
        return '{}'.format(self.engine_size)


class CarFuelType(models.Model):

    FUEL_CHOICE = (
        ('d', 'Disel'),
        ('p', 'Petrol'),
        ('h', 'Hybrid'),
        ('e', 'Electric'),
    )

    fuel = models.CharField(
        max_length=1,
        choices=FUEL_CHOICE,
        default='p',
        verbose_name='Fuel Type',
        help_text='Choose Fuel Type'
    )

    class Meta:
        unique_together = (('fuel'),)

    def __str__(self):
        return '{}'.format(self.get_fuel_display())


class CarTransmissionType(models.Model):

    TRANSISSION_CHOICE = (
        ('m', 'Manual'),
        ('a', 'Automatic'),
        ('s', 'Semi-automatic'),
    )

    transmission = models.CharField(
        max_length=1,
        choices=TRANSISSION_CHOICE,
        default='m',
        help_text='Choose transmission type'
    )

    class Meta:
        unique_together = (('transmission'),)

    def __str__(self):
        return '{}'.format(self.get_transmission_display())


class CarRegistrationNumber(models.Model):
    registration = models.CharField(
        help_text="Car Registration Number",
        max_length=15, unique=True
    )

    class Meta:
        unique_together = (('registration'),)

    def __str__(self):
        return '{}'.format(self.registration)


class CarInstance(models.Model):

    RENT_STATUS = (
        ('a', 'Available'),
        ('n', 'Not Available'),
        ('m', 'Maintenance'),
        ('r', 'Reserved'),
    )

    car_status = models.CharField(
        max_length=1,
        choices=RENT_STATUS,
        default='a',
        help_text="Car availability",
        verbose_name="Status"
    )
    car_registration = models.OneToOneField(CarRegistrationNumber)
    car = models.ForeignKey(Car)
    engine_size = models.ForeignKey(CarEngineSize, null=True, blank=True)
    fuel = models.ForeignKey(CarFuelType)
    transmission = models.ForeignKey(CarTransmissionType)
    car_specifications = models.ManyToManyField(CarSpecs, verbose_name="Specs")
    rented_to_client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Customer Name"
    )
    date_of_rent = models.DateTimeField(
        null=True, blank=True, verbose_name="Pick-up"
    )
    date_of_return = models.DateTimeField(
        null=True, blank=True, verbose_name="Drop-off"
    )

    class Meta:
        ordering = [
            "car__car_make_and_model__manufacturer_name_and_logo__manufacturer_logo_name",
            "car__car_make_and_model__manufacturer_model_name",
            "-engine_size",
            "car_status",
        ]

    def __str__(self):
        return '{} {}'.format((self.car), self.car_status)

    def get_doors_num(self):
        return self.car.num_of_doors
    get_doors_num.short_description = 'Doors'

    def get_passangers_num(self):
        return self.car.passangers
    get_passangers_num.short_description = 'Carry'

    def get_car_status(self):
        return self.get_car_status_display()

    def display_specs(self):
        specs = [spec for spec in self.car_specifications.all()]
        return specs
    display_specs.short_description = 'Specifications'

    def is_overdue(self):
        if self.date_of_return and timezone.now() > self.date_of_return:
            return True
        return False

    def clean(self):
        if self.rented_to_client and self.car_status == 'a':
            raise ValidationError("Change car status!")

    def change_car_status(self, status):
        self.car_status = status
