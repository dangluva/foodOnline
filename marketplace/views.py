from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .context_processors import get_cart_counter, get_cart_amounts
from .models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor


def martketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    check_cart.quantity += 1
                    check_cart.save()
                    return JsonResponse({'status': 'Success', 'message': "Increased the cart quantity!",
                                         'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    check_cart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': "Added the food to the cart!",
                                         'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': "This food item doesn't exist!"})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})


def remove_from_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if the user has already added that food to the cart
                try:
                    check_cart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if check_cart.quantity > 1:
                        # Decrease the cart quantity
                        check_cart.quantity -= 1
                        check_cart.save()
                    else:
                        check_cart.delete()
                        check_cart.quantity = 0
                    return JsonResponse(
                        {'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': check_cart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': "You don't have this product in your cart!"})
            except:
                return JsonResponse({'status': 'Failed', 'message': "This food item doesn't exist!"})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue.'})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'The cart item has been successfully deleted!',
                                         'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': "This cart item doesn't exist!"})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
