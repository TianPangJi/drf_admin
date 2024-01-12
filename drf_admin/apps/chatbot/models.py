from django.db import models
from django.utils.timezone import now

class ChatMessage(models.Model):
    # 機器人ID - 一個機器人，裡面有各個聊天室ID
    bot_id = models.CharField(max_length=100)

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
            self.message_id = f"{self.bot_id}-{self.chatroom_id}-{current_timestamp.strftime('%Y%m%d%H%M%S%f')}"
        super(ChatMessage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.bot_id}-{self.chatroom_id}-{self.message_id}"

    class Meta:
        # 設置數據庫表名稱
        db_table = 'chat_message'
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