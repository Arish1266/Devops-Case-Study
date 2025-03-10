from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from checkout.models import Order

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Ipswich Electronics.')
            return redirect('products:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    # Get order history
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'accounts/order_detail.html', {'order': order})
