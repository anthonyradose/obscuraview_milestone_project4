from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from django.contrib import messages
from products.models import Product


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    existing_wishlist_item = Wishlist.objects.filter(user=request.user, product=product).exists()
    if existing_wishlist_item:
        messages.info(request, f'{product.name} is already in your wishlist')
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, f'Added {product.name} to your wishlist')
    return redirect(reverse('product_detail', args=[product_id]) + '?wishlistToast=True')


@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, f'{str(wishlist_item).split("- ")[1]} removed from your wishlist')
    redirect_url = request.POST.get('redirect_url')
    return redirect(redirect_url)

