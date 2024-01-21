from rest_framework import serializers

from chatbot.models import StudentBookBot

class StudentBookBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentBookBot
        fields = ['bot_id', 'student', 'book']
