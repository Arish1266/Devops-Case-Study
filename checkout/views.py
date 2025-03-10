from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse

from cart.cart import Cart
from .models import Order, OrderItem, Coupon
from .forms import CheckoutForm, CouponForm
from products.models import Product

@login_required
def checkout_process(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        checkout_form = CheckoutForm(request.POST)
        coupon_form = CouponForm(request.POST)
        
        if checkout_form.is_valid():
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    shipping_first_name=checkout_form.cleaned_data['shipping_first_name'],
                    shipping_last_name=checkout_form.cleaned_data['shipping_last_name'],
                    shipping_address=checkout_form.cleaned_data['shipping_address'],
                    shipping_city=checkout_form.cleaned_data['shipping_city'],
                    shipping_state=checkout_form.cleaned_data['shipping_state'],
                    shipping_zip_code=checkout_form.cleaned_data['shipping_zip_code'],
                    shipping_country=checkout_form.cleaned_data['shipping_country'],
                    payment_method=checkout_form.cleaned_data['payment_method'],
                )

                # Apply coupon if valid
                if coupon_form.is_valid():
                    coupon = Coupon.objects.filter(
                        code=coupon_form.cleaned_data['code'], 
                        active=True
                    ).first()
                    if coupon and coupon.is_valid():
                        order.coupon = coupon
                        order.discount = coupon.calculate_discount(cart.get_total_price())

                # Create order items
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

                # Clear the cart
                cart.clear()

                # Redirect to order confirmation
                return redirect('checkout:order_confirmation', order_id=order.id)
    else:
        checkout_form = CheckoutForm()
        coupon_form = CouponForm()

    return render(request, 'checkout/checkout.html', {
        'checkout_form': checkout_form,
        'coupon_form': coupon_form,
        'cart': cart
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'checkout/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'checkout/order_history.html', {'orders': orders})

def apply_coupon(request):
    if request.method == 'POST':
        cart = Cart(request)
        coupon_code = request.POST.get('code', '')
        
        try:
            coupon = Coupon.objects.get(code=coupon_code, active=True)
            
            if coupon.is_valid():
                original_total = cart.get_total_price()
                discounted_total = coupon.apply_discount(original_total)
                
                return JsonResponse({
                    'success': True,
                    'original_total': original_total,
                    'discounted_total': discounted_total
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'error': 'Coupon is not valid or has expired.'
                })
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'Coupon does not exist.'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
