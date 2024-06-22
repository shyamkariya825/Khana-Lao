from django.http import HttpResponse
from django.shortcuts import render, redirect

from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages


# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request, "Your account has been created !")
            return redirect('registerUser')
        else:
            print(form.errors)


    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.method == 'POST':
        # store data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            password=form.cleaned_data['password']
            username=form.cleaned_data['username']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, contact=contact, password=password, username=username)
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user=user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request, "Your account has been created ! Please wait for approval.")
            return redirect('registerVendor')
        else:
            print('Invalid Form')
            print(form.errors)

    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form
    }
    return render(request, 'accounts/registerVendor.html', context)

