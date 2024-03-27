from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, ProfileUpdateForm

def home(request):
    return render(request, 'home.html')

def profile(request):
    return render(request, 'profile.html')

@login_required
def profileUpdateView(request):
    u_form = CustomUserChangeForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'account/update_profile.html', context)