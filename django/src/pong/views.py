from django.shortcuts import render
from utils.request_helpers import is_ajax_request
from django.contrib.auth.decorators import login_required


@login_required
def pong(request):
    if is_ajax_request(request):
        return render(request, 'components/pages/pong.html')
    return render(request, 'index.html')

