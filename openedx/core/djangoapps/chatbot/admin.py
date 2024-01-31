from django.contrib import admin
from .models import ChatbotError, ChatbotSession, ChatbotQuery

class ChatbotErrorAdmin(admin.ModelAdmin): 
    list_display = ["created", "error_msg"]

    def __str__(self, obj):
        return f"{obj.created} - {obj.error_msg[0:10]}..."

class ChatbotQueryAdmin(admin.ModelAdmin):
    list_display = ['created', 'status', 'query_msg']

    def __str__(self, obj):
        return f"{obj.created} - {obj.status} - {obj.query_msg}"

admin.site.register(ChatbotError, ChatbotErrorAdmin)
admin.site.register(ChatbotSession)
admin.site.register(ChatbotQuery, ChatbotQueryAdmin)