from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from chatbot.backend import get_gpt_response
from chatbot.models import ChatMessage
from chatbot.serializers.centre import ChatMessageSerializer  # 導入 Response

def save_chat_message(data):
    serializer = ChatMessageSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    else:
        raise ValueError(serializer.errors)

class ChatMessageUpdateAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    更新聊天訊息
    - status: 200(成功)
    - return: 修改聊天訊息
    """
    def put(self, request, *args, **kwargs):
        student_book_bot_id = request.data.get('student_book_bot_id')
        chatroom_id = request.data.get('chatroom_id')
        sender = request.data.get('sender')
        message = request.data.get('message')
        tag = '測試'

        user_data = {
            'bot_id': student_book_bot_id,
            'chatroom_id': chatroom_id,
            'sender': sender,
            'message': message,
            'tag': tag,
        }
        bot_data = {
            'bot_id': student_book_bot_id,
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
    根據 bot_id 和 chatroom_id 從數據庫檢索訊息。
    - status: 200(成功)
    - return: 取得指定 bot_id 和 chatroom_id 的聊天訊息
    """

    def get(self, request, *args, **kwargs):
        # 從請求中檢索 bot_id 和 chatroom_id。
        # 在這裡，我假設這些作為查詢參數發送。
        print('request DATA',request.query_params)
        bot_id = request.query_params.get('bot_id')
        # student_book_bot_id=1
        # # chatroom_id = request.query_params.get('chatroom_id')
        chatroom_id ='0'
        if not bot_id or not chatroom_id:
            return Response({"error": "缺少 bot_id 或 chatroom_id"}, status=400)
        print('bot_id',bot_id,'chatroom_id',chatroom_id)
        # 查詢 ChatMessage 模型
        messages = ChatMessage.objects.filter(
            bot_id=bot_id, chatroom_id=chatroom_id
        ).order_by('timestamp')  # 如果需要，按時間戳排序
        # 格式化數據
        formatted_messages = [
            {
                'userId': message.id,  # 假設您在這裡想要訊息 ID
                'sender': message.sender,
                'message': message.message
            }
            for message in messages
        ]
        print('formatted_messages',formatted_messages)
        return Response(formatted_messages)




    def get_object(self):
        return self.request.user
