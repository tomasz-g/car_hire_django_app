from datetime import date, datetime

from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.core.mail import BadHeaderError, EmailMultiAlternatives

from .forms import ContactForm
from .models import CarManufacturerAndLogo, Car, CarInstance


"""
Home page with all manufacturers logo images as a link
to a page which Display only that manufacturer car/s.
"""
class Home(generic.ListView):
    model = CarManufacturerAndLogo
    context_object_name = 'all_manufacturers'
    template_name = 'index.html'


"""
All models in company fleet.
"""
class CarsFleetListView(generic.ListView):
    template_name = 'cars_fleet/all-models.html'
    context_object_name = 'cars_fleet'
    paginate_by = 10
    queryset = Car.objects.order_by('car_type', 'car_make_and_model')


"""
All models of particular manufacturer.
"""
class ByBrandListView(generic.ListView):
    template_name = 'cars_fleet/all-models.html'
    context_object_name = 'cars_fleet'

    def get_queryset(self, *args, **kwargs):
        return Car.objects.filter(
            car_make_and_model__manufacturer_name_and_logo=self.kwargs['pk']
        )


"""
All cars options of one model with full details.
"""
class CarDetailView(generic.DetailView):
    model = Car
    context_object_name = 'cars_details'
    template_name = 'cars_fleet/cars-details.html'


"""
All cars in company fleet with full details.
! Only staff users !
"""
class AllCarsListView(PermissionRequiredMixin, generic.ListView):
    model = CarInstance
    permission_required = (
        'cars_fleet.add_carinstance',
        'cars_fleet.change_carinstance',
        'cars_fleet.delete_carinstance'
    )
    context_object_name = 'all_cars'
    template_name = 'cars_fleet/all-cars.html'
    paginate_by = 10


"""
All available cars in company fleet with full details.
! Only staff users !
"""
class AllAvailableCarsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = (
        'cars_fleet.add_carinstance',
        'cars_fleet.change_carinstance',
        'cars_fleet.delete_carinstance'
    )
    context_object_name = 'available_cars'
    template_name = 'cars_fleet/available-cars.html'
    paginate_by = 10

    queryset = CarInstance.objects.filter(car_status='a')


"""
All rented cars in company fleet with full details.
! Only staff users !
"""
class AllRentedCarsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = (
        'cars_fleet.add_carinstance',
        'cars_fleet.change_carinstance',
        'cars_fleet.delete_carinstance'
    )
    context_object_name = 'rented_cars'
    template_name = 'cars_fleet/rented-cars.html'
    paginate_by = 10

    queryset = CarInstance.objects.filter(car_status='n')


"""
All overdue cars in company fleet with full details.
! Only staff users !
"""
class AllOverdueCarsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = (
        'cars_fleet.add_carinstance',
        'cars_fleet.change_carinstance',
        'cars_fleet.delete_carinstance'
    )
    context_object_name = 'overdue_cars'
    template_name = 'cars_fleet/overdue-cars.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            CarInstance.objects.exclude(
                date_of_return__isnull=True
            ).exclude(
                date_of_return__gte=date.today()
            ).filter(
                car_status='n'
            )
        )


"""
All cars under maintenance in company fleet with full details.
! Only staff users !
"""
class AllMaintenanceCarsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = (
        'cars_fleet.add_carinstance',
        'cars_fleet.change_carinstance',
        'cars_fleet.delete_carinstance'
    )
    context_object_name = 'maintenance_cars'
    template_name = 'cars_fleet/maintenance-cars.html'
    paginate_by = 10
    queryset = CarInstance.objects.filter(car_status='m')


"""
All cars rented by particular user.
! Only logged in users !
"""
class RentedCarsByClientListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'client_cars'
    template_name = 'cars_fleet/client-cars.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            CarInstance.objects.filter(
                rented_to_client=self.request.user).order_by('date_of_return'
            )
        )

"""
View function for Contact page
"""
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_email = form.cleaned_data['contact_email']
            message_text = 'email from: {} message: {}'.format(
                                                            contact_email,
                                                            message
                                                        )
            try:
                current_time = datetime.now()
                html = get_template('cars_fleet/email_html.html')
                html_content = html.render(
                    {
                        'subject': subject,
                        'message': message,
                        'contact_email': contact_email,
                        'current_time': current_time,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject,
                    message_text,
                    contact_email,
                    ['carhiretemp@gmail.com'],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, 'cars_fleet/contact.html', {'form': form})

def thanks(request):
    return render(request, 'cars_fleet/thanks.html')
