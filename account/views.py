from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth import authenticate ,login
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
# Create your views here.

@login_required
def dashboard(request):
    print(request.method)

    return render(request,'account/dashboard.html',{'section':'dashboard'})
@login_required
def edit(request):
    if request.method == 'POST':
        print(request.method)
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile Updated successfully")
    else:
        user_form=UserEditForm(instance =request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
        messages.error(request, "Error in  Update Your Profile")
    return render (request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})
    
def register(request):
    print(1)
    user_form=UserRegistrationForm()
    if request.method == 'POST':
        print(2)
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            print(3)

            # Create a new user object but avoid saving yet
            new_user=user_form.save(commit=False)
            #Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            #Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            print(4)
            
            return render(request,'account/register_done.html',{'new_user':new_user})
        else:
            print(6)

            user_form=UserRegistrationForm()
    print(5)
    
    return render(request,'account/register.html',{'user_form':user_form})  
    
      
def user_login(request):
    if request.method =='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabeld account')
            else:
                return HttpResponse('Invaled login ')
    else:
        form =LoginForm()
    return render(request,'registration/login.html',{'form':form})
    
