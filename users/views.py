from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import AccountInformationForm, BioForm, EditProfileForm, EduForm, LoginForm, RegistrationForm, WorkForm
from users.models import AwardModel, EducationModel, ProfileModel, UserModel, WorkExperienceModel


def login_view(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user and user.is_active:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('home')
            else:
                return redirect('login')
        else:
            return render(request, 'users/login.html', {'form': form})
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            ProfileModel.objects.create(user=user)
            # send_registration_mail(user)
            return redirect('home')
        else:
            return render(request, 'users/Registration.html', {"form": form})

    form = RegistrationForm()
    context = {
        "form": form
    }
    return render(request, 'users/Registration.html', context)


@login_required(login_url='login')
def profile_view(request, pk):
    user = UserModel.objects.get(id=pk)
    profile = ProfileModel.objects.get(user=user)

    workExpList = WorkExperienceModel.objects.filter(user=user)
    eduList = EducationModel.objects.filter(user=user)
    awardList = AwardModel.objects.filter(user = user)

    is_self = False
    if user == request.user:
        is_self = True
    

    eduform = EduForm()
    if request.method == "POST":
        eduform = EduForm(request.POST)
        if eduform.is_valid():
            eduItem = eduform.save(commit=False)
            eduItem.user = user
            eduItem.save()
            return redirect("profile", user.id)

    workform = WorkForm()
    if request.method == "POST":
        workform = WorkForm(request.POST)
        if workform.is_valid():
            workItem = workform.save(commit=False)
            workItem.user = user
            workItem.save()
            return redirect("profile", user.id)
    
    form = BioForm()
    if request.method == "POST":
        form = BioForm(request.POST)
        if form.is_valid():
            profile.bio = request.POST["bio"]
            profile.save()
            return redirect("profile", user.id)

    context = {
        'profile': profile,
        'is_self': is_self,
        'workform': workform,
        'education': eduList,
        'workExp' : workExpList,
        'awards' : awardList,
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def edit_profile_view(request):
    return render(request, 'users/edit-profile.html')


# @login_required(login_url='login')
# def account_settings_view(request):
#     return render(request, )


def about_view(request):
    pass


def contact_view(request):
    pass

def account_settings(request):
    user = request.user

    information_form = AccountInformationForm(instance=user)
    password_form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        information_form = AccountInformationForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if information_form.is_valid():
            information_form.save()
            return redirect('settings')

        elif password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            context = {
                'information_form': information_form,
                'password_form': password_form,
            }
            return render(request, "users/settings.html", context)
    context = {
        'information_form': information_form,
        'password_form': password_form,
    }
    return render(request, "users/settings.html", context)

def edit_profile_view(request):
    user = request.user
    profile = ProfileModel.objects.get(user=user)
    profileForm = EditProfileForm(instance=profile)
    if request.method == "POST":
        profileForm = EditProfileForm(request.POST, request.FILES ,instance=profile)
        if profileForm.is_valid():
            profileForm.save()
            return redirect("profile", user.id)

    context = {
        'profileForm' : profileForm,
        'profile' : profile,
    }
    return render(request, 'users/edit_profile.html', context)
