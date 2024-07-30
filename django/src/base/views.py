from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm, ProfileUpdateForm
from .models import Profile


def home(request):
    return render(request, 'home.html')

def pong(request):
    return render(request, 'pong.html')

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile, 'user': user}
    return render(request, 'profile.html', context)


@login_required
def profileUpdateView(request):
    user = request.user
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'p_form': p_form}

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request, 'update_profile.html', context)


@login_required
def settings(request):
    return render(request, 'settings.html')