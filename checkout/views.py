from django.shortcuts import render, redirect, reverse

from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket at the moment")
        return redirect(reverse('products'))
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51POf7ZDeVSCa472mpwqFcKr5pHqJPOLtVI8d4wszP6yFbTRokEwd65B5F7UHcjSYK6BMlXBanCV0NfvPrVP3dprF00mnyTF68B',
        'client_secret': 'test_client_secret'
    }

    return render(request, template, context)
