from django.shortcuts import render
from utils.request_helpers import is_ajax_request

def pong(request):
    if is_ajax_request(request):
        return render(request, 'components/pong.html')
    return render(request, 'index.html')

