from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from Accounts.models import profile 
from Product.models import * 
from django.http import HttpResponse
import random

# Home view
def home(request):
    cat = Category.objects.all()
    pro = Product.objects.all()
    return render(request, 'home.html', locals())


# Registration view
def register(request):
    if request.user.is_authenticated: 
        return redirect('home')
    
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Validating the input fields
        if User.objects.filter(username=name).exists():
            error_message = "Username already exists. Please choose another one."
        elif User.objects.filter(email=email).exists():
            error_message = "Email is already registered. Please use another email."
        elif len(password) < 8:
            error_message = "Password must be at least 8 characters long."

        # If no errors, create user and profile, and send OTP email
        if not error_message:
            user = User.objects.create_user(username=name, email=email, password=password, is_active=False)
            otp = random.randint(1000, 9999)
            profile.objects.create(user=user, otp=str(otp))  # Create profile with OTP

            # Storing OTP and user_id in session
            request.session['otp'] = otp
            request.session['user_id'] = user.id

            # Sending OTP email
            subject = f'Your OTP: {otp}'
            message = f'Don\'t share your OTP: {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                error_message = "Failed to send OTP email. Please try again later."

            if not error_message:
                return redirect('verify_otp')

    return render(request, 'registration.html', {'error_message': error_message})

# Login view
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    error_message = None

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        # Validating login credentials
        if name and password:
            user = authenticate(username=name, password=password)
            if profile.objects.get(user=user).is_verified == True:
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    error_message = "Invalid username or password. Please try again."
            else:
                messages.error(request, 'Account not verified')
        else:
            error_message = "Username and password fields cannot be empty."
    
    return render(request, 'login.html', {'error_message': error_message})

# Logout view
def logout_user(request):
    logout(request)
    return redirect('login')

# Send Mail Request view
def send_mail_req(request):
    if request.method == 'POST':
        otp = random.randint(1000, 9999)
        subject = f'Your OTP: {otp}'
        message = f'Don\'t share your OTP: {otp}'
        from_email = settings.EMAIL_HOST_USER
        
        recipient_email = request.POST.get('mail_input')
        recipient_list = [recipient_email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            return HttpResponse("Failed to send email. Please try again later.")

        return redirect('home')  # Redirect to home or any other page you prefer

    return render(request, 'home.html')

# OTP Verification view
def verify_otp(request):
    error_message = None

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        user_id = request.session.get('user_id')

        # Verify OTP
        if str(entered_otp) == str(stored_otp):
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()

            # Update profile verification status
            user_profile = profile.objects.get(user=user)
            user_profile.is_verified = True
            user_profile.save()
            messages.success(request, 'Your account is verified, please Login')

            # Clear OTP session data
            del request.session['otp']
            del request.session['user_id']

            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid OTP. Please try again."

    return render(request, 'otp_verification.html', {'error_message': error_message})


# Forget Password View
def forget_pass(request):
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if email exists in the database
        try:
            user = User.objects.get(email=email)
            otp = random.randint(1000, 9999)
            
            # Save OTP to user's profile
            user_profile = profile.objects.get(user=user)
            user_profile.otp = str(otp)
            user_profile.save()

            # Send OTP email
            subject = f'Reset Your Password - OTP: {otp}'
            message = f'Use the OTP {otp} to reset your password. Don\'t share it with anyone.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list)

            # Store user_id in session for verification
            request.session['user_id'] = user.id
            return redirect('verify_user')

        except User.DoesNotExist:
            error_message = "Email not found. Please check and try again."

    return render(request, 'forget_password.html', {'error_message': error_message})

# Verify User and Reset Password View
def verify_user(request):
    error_message = None

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        user_id = request.session.get('user_id')

        # Verify OTP and reset password
        try:
            user = User.objects.get(id=user_id)
            user_profile = profile.objects.get(user=user)

            if str(entered_otp) == user_profile.otp:
                user.set_password(new_password)
                user.save()

                # Clear session and OTP
                del request.session['user_id']
                user_profile.otp = ''
                user_profile.save()

                messages.success(request, 'Password reset successful. Please log in with your new password.')
                return redirect('login')

            else:
                error_message = "Invalid OTP. Please try again."

        except User.DoesNotExist:
            error_message = "An error occurred. Please try again."

    return render(request, 'verify_user.html', {'error_message': error_message})



