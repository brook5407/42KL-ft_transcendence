from rest_framework.pagination import PageNumberPagination


class GameHistoryPagination(PageNumberPagination):
    page_size = 10