from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Review
from .forms import ReviewForm
from django.contrib import messages


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST or None)
    if request.method == 'POST':
        existing_review = Review.objects.filter(user=request.user, product=product).exists()
        if existing_review:
            messages.info(request, f'You have already reviewed {product.name}')             
        elif form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, f'Your review for {product.name} has been submitted')
            return redirect('product_detail', product_id=product.id)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, 'Review updated successfully.')
            else:
                messages.info(request, 'No changes were made.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        messages.error(request, 'Invalid request method.')
    return redirect('profile')


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)    
    if request.method == 'POST':
        review.delete()
        messages.success(request, f'{review} removed from your reviews')
        review_removed = True
        redirect_url = request.POST.get('redirect_url')
    return redirect(f"{redirect_url}?review_removed={review_removed}")

