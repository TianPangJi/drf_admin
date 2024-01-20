from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from drf_admin.apps.courses.models import Book
from drf_admin.apps.courses.serializers.books import BooksSerializer

class BooksViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):    
    """
    BooksViewSet 提供書籍的新增、更新和刪除功能
    - status: 200(成功), 400(請求錯誤), 201(創建成功), 204(刪除成功)
    - return: 回傳處理結果
    """

    queryset = Book.objects.all()
    serializer_class = BooksSerializer

    def get(self, request, *args, **kwargs):
        """
        GET 方法用於檢索書籍記錄
        - 若提供 ID，則檢索特定書籍
        - 若不提供 ID，則返回所有書籍列表
        """
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        POST 方法用於創建新的書籍記錄
        - 接收書籍的資料並嘗試進行儲存
        - 成功時返回 HTTP 201 Created 狀態
        - 失敗時返回 HTTP 400 Bad Request 狀態
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        PUT 方法用於更新現有的書籍記錄
        - 接收書籍的新資料並嘗試進行更新
        - 成功時返回 HTTP 200 OK 狀態
        - 失敗時返回 HTTP 400 Bad Request 狀態
        """
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        DELETE 方法用於刪除書籍記錄
        - 根據提供的 ID 刪除指定的書籍記錄
        - 成功時返回 HTTP 204 No Content 狀態
        """
        if 'pk' in kwargs:
            # 單獨刪除
            return self.destroy(request, *args, **kwargs)
        else:
            # 批量刪除
            ids = request.data.get('ids', [])
            if not ids:
                return Response({"detail": "未提供 ID 列表。"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                books = Book.objects.filter(book_id__in=ids)
                if not books.exists():
                    return Response({"detail": "找不到指定的書籍。"}, status=status.HTTP_404_NOT_FOUND)
                books.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
