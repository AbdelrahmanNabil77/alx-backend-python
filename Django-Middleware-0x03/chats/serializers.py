from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the custom User model."""

    full_name = serializers.SerializerMethodField()  # ✔️ Using SerializerMethodField

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'full_name',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message objects, includes sender info."""

    sender_username = serializers.CharField(
        source='sender.username', read_only=True)  # ✔️ Using CharField

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'sender_username',
            'message_body',
            'sent_at',
        ]

    def validate_message_body(self, value):
        """Ensure the message body isn't empty or just whitespace."""
        if not value.strip():
            raise serializers.ValidationError(
                "Message body cannot be empty.")  # ✔️ Using ValidationError
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation, including participants and messages."""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]
