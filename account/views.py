from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages 
import os 

from .models import Profile
from .forms import ProfileForm

from blog.models import Post 

# Create your views here.  
class AccountMixin(object):
    def dispatch(self, request, *args, **kwargs): 
        if request.user.is_authenticated:
            pass 
        else:
            messages.success(request, 'User should be logged-in before performing the operation.')
            return redirect("account:login")
        return super().dispatch(request, *args, **kwargs)

class UserSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("blog:home")
        form = UserCreationForm()
        return render(request, 'account/signup.html',{'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Created successfylly. Login here')
            return redirect('account:login')
        return render(request, 'account/signup.html', {'form': form})

class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("blog:home")
        form = AuthenticationForm()
        return render(request, 'account/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request=request, data = request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pword = form.cleaned_data['password']
            user = authenticate(username=uname, password=pword)
            if user is not None:
                login(request, user) 
                # messages.success(request, "Login successful !")
                return redirect("blog:home")
        return render(request, 'account/login.html', {'form':form})

class ProfileView(AccountMixin, View):
    def get(self, request):  
        posts = request.user.posts.all().order_by("-id")
        return render(request, "account/profile.html", {'posts': posts})

class PassswordChangeView(AccountMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user = request.user)
        return render(request, "account/changepassword1.html", {'form': form})

    def post(self,request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed successfully !!!")
            return redirect('account:profile')
        return render(request, "account/changepassword1.html", {'form': form})


class ProfileUpdateView(AccountMixin, View):
    def get(self, request):
        profile = Profile.objects.get(user = request.user)
        update_form = ProfileForm(instance=profile) 
        return render(request, 'account/update_profile.html', {"update_form": update_form})

    def post(self, request):
        profile = Profile.objects.get(user = request.user) 
        previous_image_path = ""
        if profile.image != "":
            previous_image_path = profile.image.path 
        update_form = ProfileForm(request.POST, request.FILES, instance=profile)  
        if update_form.is_valid():
            if  update_form.cleaned_data['image'] is not None: 
                if os.path.exists(previous_image_path): 
                    os.remove(previous_image_path)
                update_form.save()  
                messages.success(request, "Profile is update successfully and old image is removed if exists.") 
            return redirect("account:profile") 
        return render(request, 'account/update_profile.html', {"update_form": update_form})


def UserLogout(request):
    logout(request)
    return redirect("account:login")