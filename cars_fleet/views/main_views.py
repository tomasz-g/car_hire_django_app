from django.views import generic
from cars_fleet.models import CarManufacturerAndLogo


"""
Home page with all manufacturers logo images as a link
to a page which Display only that manufacturer car/s.
"""
class Home(generic.ListView):
    model = CarManufacturerAndLogo
    context_object_name = 'all_manufacturers'
    template_name = 'index.html'
