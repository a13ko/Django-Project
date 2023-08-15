from django.shortcuts import render
from .models import MyUser

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import (
    LoginForm, RegisterForm, ActivateForm, CustomPasswordChangeForm,
    ResetPasswordForm, ResetPasswordCompleteForm,UserDataChangeForm
)
from django.contrib.auth.decorators import login_required
from .decorators import not_authorized_user
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

User = get_user_model()

@not_authorized_user
def login_view(request):
    next = request.GET.get("next", None)
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST or None)

        if form.is_valid():

            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            login(request, user)
            if next:
                return redirect(next)
            return redirect('/')

    context = {
        "form": form
    }
    return render(request,"users/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save()

            return redirect("users:activate", slug=user.slug)

    context = {
        "form": form
    }
    return render(request, "users/register.html", context)



def account_activate_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = ActivateForm()

    if request.method == "POST":
        form = ActivateForm(request.POST or None)

        if form.is_valid():
            form.save(user=user)
            # login(request, user)
            return redirect('users:login')


    context = {
        "form": form
    }
    return render(request, "users/activate.html", context)

@login_required(login_url='/users/login/')
def password_change_view(request):
    form = CustomPasswordChangeForm(user=request.user)

    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('//')

    context = {
        "form": form
    }
    return render(request, "users/password_change.html", context)



def reset_password_view(request):
    form = ResetPasswordForm()

    if request.method == "POST":
        form = ResetPasswordForm(request.POST or None)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)

            link = request.build_absolute_uri(reverse_lazy("users:reset-complete", kwargs={"slug": user.slug}))
            message = f"Please click the link below \n{link}"


            # send mail
            send_mail(
                'Reset password',  # subject
                message,  # message
                settings.EMAIL_HOST_USER,  # from email
                [email],  # to mail list
                fail_silently=False,
            )

            return redirect("/users/before-reset/")

    context = {
        "form": form
    }
    return render(request, "users/reset.html", context)



def reset_password_complete_view(request, slug):
    user = get_object_or_404(User, slug=slug)
    form = ResetPasswordCompleteForm(instance=user)

    if request.method == "POST":

        form = ResetPasswordCompleteForm(instance=user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect("/users/login/")

    context = {
        "form": form
    }
    return render(request, 'users/reset_complete.html', context)





def before_reset(request):
    return render(request,'users/before_reset.html',{})





def show_privacy(request):
    return render(request, 'users/privacy.html',{})





# def profile(request):
#     profiles = User.objects.all()
#     if request.method == 'POST':
#         form = UserDataChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('/users/profile') 
#     else:
#         form = UserDataChangeForm(instance=request.user)
    
#     return render(request, 'users/profile.html',{'form': form,'profiles':profiles})


def profile(request):
    profiles = User.objects.all()
    if request.method == 'POST':
        form = UserDataChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/users/profile')
      
    else:
        form = UserDataChangeForm(instance=request.user)

    return render(request, 'users/profile.html',{'form': form,'profiles':profiles})



def plan(request):
    return render(request,'users/pricing.html',{})

def faq(request):
    return render(request,'users/faq.html',{})
    


@login_required(login_url='/users/login/')
def checkout(request):
    if request.method == 'POST':
        payment_plan = request.POST.get('payment_plan', None)
        
        if payment_plan:
            user = User.objects.get(id=request.user.id)
            if payment_plan == 'Basic':
                user.account = 'Basic'
            elif payment_plan == 'Premium':
                user.account = 'Premium'
            user.save()
            messages.success(request, 'Odenis ugurla tamamlandi ')
            return redirect('movies:home')
    return render(request, 'users/payment.html', {})