from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.models import StudentBookBot
from chatbot.serializers.bookbot import StudentBookBotSerializer

class StudentBookBotView(APIView):
    def get(self, request, user_id, book_id, format=None):
        try:
            student_book_bot = StudentBookBot.objects.get(student_id=user_id, book_id=book_id)
            serializer = StudentBookBotSerializer(student_book_bot)
            return Response(serializer.data)
        except StudentBookBot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        fake_data = {
            'student': 1,
            'book': 13,
        }
        print('ggggggggggg')
        print(fake_data)
        serializer = StudentBookBotSerializer(data=fake_data)
        # serializer = StudentBookBotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id, book_id, format=None):
        try:
            student_book_bot = StudentBookBot.objects.get(student_id=user_id, book_id=book_id)
            serializer = StudentBookBotSerializer(student_book_bot, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StudentBookBot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
