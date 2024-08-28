# from django.contrib import admin
# from .models import ChatMessage, ChatRoom

# @admin.register(ChatRoom)
# class ChatRoomAdmin(admin.ModelAdmin):
#     list_display = ('name', 'is_public', 'cover_image_thumbnail', 'is_group_chat')
#     filter_horizontal = ('members',)  # Only use filter_horizontal for ManyToManyField
#     filter_vertical = ('messages',)   # Valid if 'messages' is ManyToManyField
#     list_filter = ('is_public',)
    
#     def cover_image_thumbnail(self, obj):
#         if obj.cover_image:
#             return f'<img src="{obj.cover_image.url}" width="100" height="100"/>'
#         return "No Image"
#     cover_image_thumbnail.allow_tags = True
#     cover_image_thumbnail.short_description = 'Cover Image Preview'

# @admin.register(ChatMessage)
# class ChatMessageAdmin(admin.ModelAdmin):
#     list_display = ('sender', 'receiver', 'room', 'timestamp', 'message')
#     search_fields = ('message',)
#     list_filter = ('sender', 'receiver', 'room', 'timestamp')



