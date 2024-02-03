from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from auth_app.forms import LoginForm, UserRegistrationForm
from auth_app.models import CustomUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def home_view(request):
    
    # subject = 'Password Reset Request'
    # message = 'message'
    # send_mail(
    #     subject, 
    #     message, 
    #     settings.EMAIL_HOST_USER,
    #     ['iamacpanjan@gmail.com'],
    #     fail_silently=False
    #     )
    return render(request, 'auth_app/home.html')

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('login_view')  
    else:
        form = UserRegistrationForm()

    return render(request, 'auth_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('profile_view')  # Redirect to the profile page
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()

    return render(request, 'auth_app/login.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'auth_app/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('home_view')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Generate a token for password reset
            token = default_token_generator.make_token(user)

            #saving expiry time and token in user table
            expiry_time = timezone.now() + timedelta(hours=1)
            user.reset_token = token
            user.reset_token_expiry = expiry_time
            user.save()

            # Create a reset password link with the token
            reset_url = reverse('reset_password', args=[urlsafe_base64_encode(force_bytes(user.pk)), token])

            # Send a password reset email
            subject = 'Password Reset Request'
            message = render_to_string('auth_app/password_reset_email.html', {'reset_url': reset_url})
            send_mail(
                subject, 
                message, 
                settings.EMAIL_HOST_USER,
                [user.email]
                )
            messages.success(request, 'Password reset email sent. Check your inbox.')
            render(request, 'auth_app/forgot_password.html')

    return render(request, 'auth_app/forgot_password.html')

def reset_password_view(request, pk, token):
    try:
        user_pk = force_str(urlsafe_base64_decode(pk))
        user = CustomUser.objects.get(pk=user_pk)
        
         # Check if the reset token is still valid
        if user.reset_token_expiry < timezone.now():
            # Token has expired, handle accordingly (e.g., redirect to a new password reset request)
            return render(request, 'password_reset_expired.html')


        # Check if the token is valid
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password = request.POST.get('new_password')
                user.reset_token = None
                user.reset_token_expiry = None
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('login_view')

            return render(request, 'auth_app/reset_password.html', {'token': token})
        else:
            messages.error(request, 'Invalid token. Please request a new password reset.')
            return redirect('login_view')

    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        messages.error(request, 'Invalid token. Please request a new password reset.')
        return redirect('login_view')