from django.contrib import admin

from .models import CarModel, CarManufacturerAndLogo
from .models import Car, CarSpecs, BodyType, CarType
from .models import CarInstance, CarEngineSize
from .models import CarFuelType, CarTransmissionType
from .models import CarRegistrationNumber


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    fields = [
        'manufacturer_name_and_logo',
        'manufacturer_model_name',
    ]


@admin.register(CarManufacturerAndLogo)
class CarManufacturerAndLogoAdmin(admin.ModelAdmin):
    pass


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'car_make_and_model',
        'get_car_type',
        'get_car_body',
        'num_of_doors',
        'passangers',
    )

    fields = [
        'car_make_and_model',
        'car_type',
        'car_body',
        'num_of_doors',
        'passangers',
        'car_image',
    ]


@admin.register(CarSpecs)
class CarSpecsAdmin(admin.ModelAdmin):
    pass


@admin.register(BodyType)
class BodyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CarEngineSize)
class CarEngineSizeAdmin(admin.ModelAdmin):
    pass


@admin.register(CarFuelType)
class CarFuelTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CarTransmissionType)
class CarTransmissionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CarRegistrationNumber)
class CarRegistrationNumberAdmin(admin.ModelAdmin):
    pass


@admin.register(CarInstance)
class CarInstanceAdmin(admin.ModelAdmin):
    empty_value_display = 'N/A'

    list_filter = (
        'car_status',
        'date_of_return',
        'car__car_type',
    )

    list_display = (
        'car',
        'engine_size',
        'fuel',
        'transmission',
        'get_doors_num',
        'get_passangers_num',
        'display_specs',
        'car_status',
        'date_of_return_view',
        'rented_to_client',
    )

    fields = [
        'car_registration',
        'car',
        'engine_size',
        'fuel',
        'transmission',
        'car_specifications',
        'car_status',
        'rented_to_client',
        'date_of_return',
    ]

    def date_of_return_view(self, obj):
        return obj.date_of_return

    date_of_return_view.empty_value_display = 'unknown'
    date_of_return_view.short_description = 'Date of Return'
