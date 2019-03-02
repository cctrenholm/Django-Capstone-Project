from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import send_mail
from django.conf import settings

#uses django built-in user creation form on registration page
def register(request):
    #if get POST request create user form w/ POST data user filled in or create blank form
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #form data vailidation, save in form.cleaned dict
        if form.is_valid():
            #saves user data & hashes passwrod            
            form.save()
            username = form.cleaned_data.get('username')
           #built in flash message alterts user account creation successful 
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    #if request is a POST create two forms> update & profile
    if request.method == 'POST':
        #get user data with instance request, FILES handles uploaded photos
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                #get user profile with instance request
                                   instance=request.user.profile)
        #check is valid before saving data
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            #show flash message that the account was updated
            messages.success(request, f'Account updated')
            #back to profile page
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)