from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserChangeForm, ProfileUpdateForm
from .models import Profile


def home(request):
    return render(request, 'home.html')


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile, 'user': user}
    return render(request, 'profile.html', context)


@login_required
def profileUpdateView(request):
    u_form = CustomUserChangeForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'account/update_profile.html', context)
