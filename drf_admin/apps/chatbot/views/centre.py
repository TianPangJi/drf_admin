from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from chatbot.backend import get_gpt_response
from chatbot.models import ChatMessage
from chatbot.serializers.centre import ChatMessageSerializer  # 導入 Response


class SaveMessageAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    post:
    个人中心--修改个人信息

    个人中心修改个人信息, status: 200(成功), return: 修改后的个人信息
    """

    def put(self, request, *args, **kwargs):
        # return self.update(request, *args, **kwargs)
        message=get_gpt_response(request.data['message'])
        return Response({'userId': 1, 'sender': 'bot', 'message': message})

    def get_object(self):
        return self.request.user
    
def save_chat_message(data):
    serializer = ChatMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValueError(serializer.errors)
class ChatMessageUpdateAPIView(mixins.UpdateModelMixin, GenericAPIView):
    #TODO: update message to database

    # serializer_class = ChatMessageSerializer(data=data)

    def put(self, request, *args, **kwargs):
        bot_id = 0
        chatroom_id = 0
        sender = request.data.get('sender')
        message = request.data.get('message')
        tag = '測試'

        user_data = {
            'bot_id': bot_id,
            'chatroom_id': chatroom_id,
            'sender': sender,
            'message': message,
            'tag': tag,
        }
        bot_data = {
            'bot_id': bot_id,
            'chatroom_id': chatroom_id,
            'sender': 'bot',
            'message': get_gpt_response(message),
            'tag': tag,
        }

        try:
            with transaction.atomic():
                # 保存用戶消息
                user_response = save_chat_message(user_data)
                # 保存機器人回復
                bot_response = save_chat_message(bot_data)
                return Response({
                    'user_message': user_response,
                    'bot_message': bot_response
                }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


    def get_object(self):
        # 根据您的需求获取 ChatMessage 对象
        # 例如，可以使用 URL 中的 ID 来查找特定消息
        message_id = self.kwargs.get('id')
        return ChatMessage.objects.get(message_id=message_id)

class GetMessageAPIView(mixins.UpdateModelMixin, GenericAPIView):
    #TODO: get message from database
    """
    post:
    个人中心--修改个人信息

    个人中心修改个人信息, status: 200(成功), return: 修改后的个人信息
    """

    def get(self, request, *args, **kwargs):
        # return self.update(request, *args, **kwargs)
        # message=get_gpt_response(request.data['message'])
        messages = [
            {'userId': 1, 'sender': 'bot', 'message': 'Sample Message 1'},
            {'userId': 2, 'sender': 'user', 'message': 'Sample Message 2'}
        ]
        return Response(messages)

    def get_object(self):
        return self.request.user
