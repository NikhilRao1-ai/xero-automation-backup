from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.message} at {self.timestamp}"

class QuestionAnswer(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords for matching")

    def __str__(self):
        return self.question
