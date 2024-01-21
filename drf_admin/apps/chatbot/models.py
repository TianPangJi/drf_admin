import uuid
from django.db import models
from django.utils.timezone import now
from drf_admin.apps.courses.models import Book

from oauth.models import Users
class StudentBookBot(models.Model):
    """
    學生書籍機器人模型
    """
    bot_id = models.BigAutoField(primary_key=True, verbose_name='機器人ID')

    student = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='學生')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='書籍')

    class Meta:
        unique_together = ('student', 'book')
        verbose_name = '學生書籍機器人'


    def __str__(self):
        return f'{self.student.username} - {self.book.name}'

# on_delete=models.CASCADE 表示如果相關的 StudentBookBot 被刪除，那麼相應的 ChatMessage 記錄也會被刪除，這有助於保持數據的一致性。
# related_name='chat_messages' 允許您從 StudentBookBot 實例反向查詢到所有相關的 ChatMessage 實例。
class ChatMessage(models.Model):
    # 機器人ID - 一個機器人，裡面有各個聊天室ID
    # student_book_bot = models.ForeignKey(StudentBookBot, on_delete=models.CASCADE, related_name='chat_messages', verbose_name='學生書籍機器人',default=1)
    student_book_bot = models.ForeignKey(StudentBookBot, on_delete=models.CASCADE, related_name='chat_messages', verbose_name='學生書籍機器人',default=1)
    # student_book_bot = models.CharField(max_length=100,default=1)


    # 聊天室ID - 同一個聊天室的訊息，聊天室ID都一樣
    chatroom_id = models.CharField(max_length=100)

    # 角色sender - 表明訊息是由用戶還是機器人發送
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES)

    # message - 訊息內容
    message = models.TextField()

    # 標籤 - 訊息的標籤，可選
    tag = models.CharField(max_length=50, blank=True)

    # 訊息編號 - 自定義格式的唯一識別符
    message_id = models.CharField(max_length=255, unique=True, editable=False)

    # 訊息時間戳 - 記錄訊息的發送時間
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.message_id:
            # 生成訊息編號
            current_timestamp = now()
            self.message_id = f"{self.student_book_bot_id}-{self.chatroom_id}-{current_timestamp.strftime('%Y%m%d%H%M%S%f')}"
        super(ChatMessage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_book_bot_id}-{self.chatroom_id}-{self.message_id}"

    class Meta:
        # 設置對象的可讀名稱
        verbose_name = '聊天訊息'
        verbose_name_plural = '聊天訊息'
# Create your models here.
# 閱讀紀錄(這些訊息共用一個流水號)
# 機器人ID
# 角色 sender(user or bot)
# message
# 標籤
# 訊息編號(自動生成 1,2,3.....~)
# 訊息時間戳
        
