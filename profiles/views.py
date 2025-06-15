from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from wishlist.models import Wishlist
from reviews.models import Review
from reviews.forms import ReviewForm
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist_items = Wishlist.objects.select_related('product').filter(user=request.user)
    user_reviews = Review.objects.select_related('product', 'user').filter(user=request.user)
    review_forms = [ReviewForm(instance=review) for review in user_reviews]

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.prefetch_related('lineitems__product').all()
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'wishlist_items': wishlist_items,
        'on_profile_page': True,
        'user_reviews': user_reviews,
        'review_forms': review_forms,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order.objects.prefetch_related('lineitems__product'), order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }
    return render(request, template, context)
