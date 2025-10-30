from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Allows only participants of a conversation to perform actions on messages.
    All logic is handled in has_object_permission, including authentication and method checks.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        conversation = getattr(obj, 'conversation', obj)

        is_participant = request.user in conversation.participants.all()
        if not is_participant:
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:  # View messages
            return True
        elif request.method == 'POST':  # Send message
            return True
        elif request.method in ['PUT', 'PATCH']:  # Edit message
            return True
        elif request.method == 'DELETE':  # Delete message
            return True

        return False
