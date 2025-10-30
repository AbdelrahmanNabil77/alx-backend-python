import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom User model with additional fields."""
    user_id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    password = models.CharField(max_length=128)

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELD = 'username'  # You can switch this to 'email' if needed

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """Tracks which users are in a conversation."""
    conversation_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """Message model linking sender and conversation."""
    message_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"
