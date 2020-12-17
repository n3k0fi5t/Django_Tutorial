from http import HTTPStatus

from django.contrib.auth import logout
from django.utils.decorators import method_decorator

from utils.api import APIView, validate_serializer

from account.permissions import (
    login_required,
    check_object_permission
)

from .models import TodoItem
from .serializers import EditTodoItemSerializer, TodoItemCreateSerializer, TodoItemSerializer

# Create your views here.
class TodoItemListAPIView(APIView):
    @login_required
    def get(self, request):
        user = request.user

        items = user.todoitem_set.all()
        return self.success(
            TodoItemSerializer(items, many=True).data
        )

    @validate_serializer(TodoItemCreateSerializer)
    @login_required
    def post(self, request):
        user = request.user
        data = request.data

        todo_item = TodoItem.objects.create(
            user=user,
            title=data.get('title'),
            content=data.get('content', '')
        )

        return self.success(
            TodoItemSerializer(todo_item).data
        )

class TodoItemAPIView(APIView):
    @login_required
    def dispatch(self, request, id, *args, **kwargs):
        user = request.user
        try:
            todo_item = TodoItem.objects.select_related('user').get(id=id)
            if not check_object_permission(todo_item, user):
                return self.error(HTTPStatus.FORBIDDEN, err="permission deny")

            return super().dispatch(request, todo_item)
        except TodoItem.DoesNotExist:
            return self.error(HTTPStatus.BAD_REQUEST, err="Todo item does not exist")

    def get(self, request, todo_item):
        return self.success(
            TodoItemSerializer(todo_item).data
        )

    @validate_serializer(EditTodoItemSerializer)
    def put(self, request, todo_item):
        data = request.data

        for k, v in data.items():
            setattr(todo_item, k, v)

        todo_item.save()
        return self.success(
            TodoItemSerializer(todo_item).data
        )