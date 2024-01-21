from rest_framework import serializers
from chatbot.models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['student_book_bot_id', 'chatroom_id', 'sender', 'message', 'tag', 'message_id', 'timestamp']
        read_only_fields = ['message_id', 'timestamp']

    # 如果您需要在保存之前进行任何自定义验证或处理，可以在这里添加
