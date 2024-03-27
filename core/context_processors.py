from base.models import Profile

def user_avatar(request):
    if request.user.is_authenticated:
        avatar = Profile.objects.get(user=request.user).avatar
        return {'user_avatar': avatar}
    return {}