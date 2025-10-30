from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet, UserRegisterAPIView

#Base router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

#Nested Router for messages under conversations
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
    path('register/', UserRegisterAPIView.as_view(), name='register')
]