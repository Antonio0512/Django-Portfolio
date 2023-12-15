import os

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
from .forms import ContactForm


class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()
        context['services'] = Service.objects.all()
        context['works'] = RecentWork.objects.all()
        context['client'] = Client.objects.first()
        return context


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            full_message = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
            try:
                send_mail(
                    subject=f'Message from {name}',
                    message=full_message,
                    from_email=os.environ.get("EMAIL_HOST_USER"),
                    recipient_list=[os.environ.get("EMAIL_HOST_USER")],
                    fail_silently=False,
                )
                messages.success(request, 'Message sent successfully')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, 'Form validation failed')
    else:
        form = ContactForm()

    return redirect("home")
