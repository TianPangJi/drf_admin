from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from chatbot.backend import get_gpt_response  # 導入 Response


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
