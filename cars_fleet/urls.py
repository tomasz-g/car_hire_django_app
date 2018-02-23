from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import main_views
from .views import cars_views
from .views import forms_views


# URLs available for all users
urlpatterns = [
    url(r'^$', main_views.Home.as_view(), name='index'),
    url(r'^all-models/$', cars_views.CarsFleetListView.as_view(), name='all-models'),
    url(r'^one-brand/(?P<pk>\d+)$', cars_views.ByBrandListView.as_view(), name='one-brand-cars'),
    url(r'^car/(?P<pk>\d+)$', cars_views.CarDetailView.as_view(), name='car-detail'),
    url(r'^contact/$', forms_views.contact, name='contact'),
    url(r'^signup/$', forms_views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        forms_views.activate, name='activate'),
]

# URLs available only for users with staff permissions
urlpatterns += [
    url(r'^all-cars/$', cars_views.AllCarsListView.as_view(), name="all-cars"),
    url(r'^all-available/$', cars_views.AllAvailableCarsListView.as_view(), name="all-available"),
    url(r'^all-rented/$', cars_views.AllRentedCarsListView.as_view(), name="all-rented"),
    url(r'^all-overdue/$', cars_views.AllOverdueCarsListView.as_view(), name="all-overdue"),
    url(r'^all-maintenance/$', cars_views.AllMaintenanceCarsListView.as_view(), name="all-maintenance"),
]

# URLs available only for logged in users
urlpatterns += [
    url(r'^myaccount/$', cars_views.RentedCarsByClientListView.as_view(), name="client-cars"),
    url(r'^rent-date-pick/(?P<pk>\d+)$', forms_views.rent_car, name="rent-date-pick"),
]

urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^humans.txt/$', TemplateView.as_view(template_name="humans.txt")),
]

urlpatterns += [
    url(r'^acc_activation_confirm/$', TemplateView.as_view(template_name="registration/acc_activation_confirm.html")),
    url(r'^password_reset_form/$', TemplateView.as_view(template_name="registration/password_reset_form.html")),
]
