from django.conf.urls import url, include
from django.views.generic import TemplateView

from . import views

# URLs available for all users
urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),
    url(r'^all-models/$', views.CarsFleetListView.as_view(), name='all-models'),
    url(r'^one-brand/(?P<pk>\d+)$', views.ByBrandListView.as_view(), name='one-brand-cars'),
    url(r'^car/(?P<pk>\d+)$', views.CarDetailView.as_view(), name='car-detail'),
]

# URLs available only for users with staff permissions
urlpatterns += [
    url(r'^all-cars/$', views.AllCarsListView.as_view(), name="all-cars"),
    url(r'^all-available/$', views.AllAvailableCarsListView.as_view(), name="all-available"),
    url(r'^all-rented/$', views.AllRentedCarsListView.as_view(), name="all-rented"),
    url(r'^all-overdue/$', views.AllOverdueCarsListView.as_view(), name="all-overdue"),
    url(r'^all-maintenance/$', views.AllMaintenanceCarsListView.as_view(), name="all-maintenance"),
]

# URLs available only for logged in users
urlpatterns += [
    url(r'^myaccount/$', views.RentedCarsByClientListView.as_view(), name="client-cars"),
]


urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^humans.txt/$', TemplateView.as_view(template_name="humans.txt")),
]
