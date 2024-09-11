from rest_framework.pagination import PageNumberPagination

class ChatMessagePagination(PageNumberPagination):
    page_size = 10
    

class ActiveChatRoomsPagination(PageNumberPagination):
    page_size = 10
