from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.core.mail import (
    BadHeaderError, EmailMultiAlternatives, EmailMessage
)
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth.models import User
from cars_fleet.forms import ContactForm, SignUpForm, RentCarDateForm
from cars_fleet.tokens import acc_activation_token

from cars_fleet.models import CarInstance, Car
from django.views import generic


"""
View function for contact.html page
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
            try:
                current_time = timezone.now()
                current_zone = timezone.get_current_timezone_name()
                html = get_template('cars_fleet/web_email.html')
                html_content = html.render(
                    {
                        'subject': subject,
                        'message': message,
                        'contact_email': contact_email,
                        'current_time': current_time,
                        'current_zone': current_zone,
                    }
                )
                msg = EmailMessage(
                    subject,
                    html_content,
                    contact_email,
                    ['carhiretemp@gmail.com'],
                )
                msg.content_subtype = 'html'
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'cars_fleet/thanks.html')
    return render(request, 'cars_fleet/contact.html', {'form': form})

"""
View function for signup.html page
"""
def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
    else:
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            subject = 'Activate Your Car Hire account.'
            current_site = get_current_site(request)
            user_email = form.cleaned_data.get('email')
            text_message = render_to_string(
                'registration/activate_acc_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': acc_activation_token.make_token(user),
                }
            )
            html_message = render_to_string(
                'registration/activate_acc_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': acc_activation_token.make_token(user),
                }
            )
            msg = EmailMultiAlternatives(
                subject, text_message, 'carhiretemp@gmail.com', [user_email],
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            on_page_text = 'Please check your email to confirm registration.'
            return render(request,
                'registration/acc_activation_confirm.html', {
                'text': on_page_text
                }
            )
    return render(request, 'registration/signup.html', {'form': form})

"""
Activate account email
"""
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and acc_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        on_page_text = """Thank you for your email confirmation,
                          you can log in now."""
        return render(request,
            'registration/acc_activation_confirm.html', {
            'text': on_page_text,
            }
        )
    else:
        on_page_text = 'Activation link is invalid!'
        return render(request,
            'registration/acc_activation_confirm.html', {
            'text': on_page_text,
            }
        )

# Pick a date Form
def rent_car(request, pk):
    car = get_object_or_404(CarInstance, pk=pk)
    if request.method == 'GET':
        form = RentCarDateForm(
            initial={
                'date_of_rent': timezone.now(),
                'date_of_return': timezone.now() + timezone.timedelta(days=1)
            }
        )
    else:
        form = RentCarDateForm(request.POST)
        if form.is_valid():
            user = request.user.get_username()
            on_page_text = 'Thank you {}.<br/>{} has been booked.'.format(
                user, car.car.car_make_and_model,
            )
            car.car_status = 'n'
            car.rented_to_client = request.user
            car.date_of_rent = form.cleaned_data['date_of_rent']
            car.date_of_return = form.cleaned_data['date_of_return']
            car.save()
            return render(request,
                'registration/acc_activation_confirm.html', {
                'text': on_page_text,
                }
            )

    return render(request,
        'cars_fleet/rent_car_date.html', {'form': form, 'car': car,})
