from django.contrib import admin
from .models import ChatMessage, QuestionAnswer

admin.site.register(ChatMessage)
admin.site.register(QuestionAnswer)
