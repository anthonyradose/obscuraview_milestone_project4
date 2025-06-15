from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm
from reviews.models import Review
from reviews.forms import ReviewForm
from django.db.models.functions import Lower


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.select_related('category').all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    current_sorting = f'{sort}_{direction}'

    # Get recently viewed products from session
    recently_viewed_products = request.session.get('recently_viewed', [])

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'recently_viewed_products': recently_viewed_products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product.objects.select_related('category').prefetch_related('reviews'), pk=product_id)
    reviews = product.reviews.all()
    if request.user.is_authenticated:
        existing_review = reviews.filter(user=request.user).exists()
    else:
        existing_review = False
    existing_reviews = reviews.exists()
    form = ReviewForm()
    average_rating = product.average_rating()

    # Handle recently viewed products
    recently_viewed = request.session.get('recently_viewed', [])
    print("Before update - Session data:", recently_viewed)  # Debug print
    
    # Create product dict for session
    product_dict = {
        'id': str(product.id),
        'name': str(product.name),
        'image_url': str(product.image.url) if product.image else ''
    }
    print("Current product dict:", product_dict)  # Debug print
    
    # Remove if already in list
    recently_viewed = [p for p in recently_viewed if p['id'] != str(product.id)]
    
    # Add to front of list
    recently_viewed.insert(0, product_dict)
    
    # Keep only last 5 viewed products
    recently_viewed = recently_viewed[:5]
    
    # Update session
    request.session['recently_viewed'] = recently_viewed
    request.session.modified = True
    print("After update - Session data:", recently_viewed)  # Debug print

    context = {
        'product': product,
        'reviews': reviews,
        'existing_review': existing_review,
        'existing_reviews': existing_reviews,
        'form': form,
        'average_rating': average_rating,
        'recently_viewed_products': recently_viewed
    }
    print("Context recently_viewed_products:", context['recently_viewed_products'])  # Debug print

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
