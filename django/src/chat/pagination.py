from rest_framework.pagination import PageNumberPagination

class ChatMessagePagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to modify page size
    max_page_size = 100  # Max page size
    

class ActiveChatRoomsPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to modify page size
    max_page_size = 20  # Max page size
