from django.http import HttpRequest


def is_ajax_request(request: HttpRequest):
	return request.headers.get('x-requested-with') == 'XMLHttpRequest'