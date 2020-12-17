from http import HTTPStatus
from datetime import datetime

from django.contrib.auth import logout
from django.utils.decorators import method_decorator

from utils.api import (
    APIView,
    APIError,
    validate_serializer,
    paginate_data
)

from account.permissions import (
    login_required,
    check_object_permission
)

from .models import TodoItem
from .serializers import (
    TodoItemSerializer,
    TodoItemCreateSerializer, 
    TodoItemEditSerializer, 
)

# Create your views here.
class TodoItemAPIView(APIView):
    @login_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user = request.user
        item_id = request.GET.get('item_id')
        if item_id:
            item = self._get_user_item(request)
            return self.success(TodoItemSerializer(item).data)

        items = TodoItem.objects.filter(user=user)
        data = paginate_data(request, items, TodoItemSerializer)

        return self.success(data)

    @validate_serializer(TodoItemCreateSerializer)
    def post(self, request):
        user = request.user
        data = request.data

        todo_item = TodoItem.objects.create(
            user=user,
            title=data.get('title'),
            content=data.get('content', '')
        )

        return self.success(
            TodoItemSerializer(todo_item).data,
            status=HTTPStatus.CREATED
        )

    @validate_serializer(TodoItemEditSerializer)
    def put(self, request):
        item = self._get_user_item(request)

        data = request.data
        for k, v in data.items():
            setattr(item, k, v)

        if data.get("is_finished"):
            item.finish_time = datetime.now()

        item.save()
        return self.success(TodoItemSerializer(item).data)

    def delete(self, request):
        item = self._get_user_item(request)
        item.delete()
        return self.success("delete sucessfully")

    def _get_user_item(self, request):
        item_id = request.GET.get("item_id")
        user = request.user
        try:
            todo_item = TodoItem.objects.select_related('user').get(id=item_id)
            if not check_object_permission(todo_item, user):
                raise APIError(HTTPStatus.FORBIDDEN, err="item is not allowed query by this user")

            return todo_item
        except TodoItem.DoesNotExist:
            raise APIError(HTTPStatus.BAD_REQUEST, err="Todo item does not exist")
