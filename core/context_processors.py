from base.models import Profile


def user_avatar(request):
    if request.user.is_authenticated:
        avatar = Profile.objects.get(id=request.user.id).avatar
        return {'user_avatar': avatar}
    return {}
