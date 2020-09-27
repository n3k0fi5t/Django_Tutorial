from django.shortcuts import render, reverse, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.conf import settings
from django.utils import timezone

from .models import TodoItem

@login_required
def delete_todo_item(request, todo_id):
    try:
        item = TodoItem.objects.get(id=todo_id, user=request.user)
        item.delete()
    except TodoItem.DoesNotExist:
        pass

    return redirect(reverse('todo:list'))

@login_required
def cross_off_item(request, todo_id):
    try:
        item = TodoItem.objects.select_for_update().get(id=todo_id, user=request.user)
        with transaction.atomic():
            item.is_cross_off = True
            item.finish_time = timezone.now()
            item.save(update_fields=['is_cross_off', 'finish_time'])
    except TodoItem.DoesNotExist:
        pass

    return redirect(reverse('todo:list'))

# Create your views here.
class TodoView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kargs):
        return super(TodoView, self).dispatch(request, *args, **kargs)

    def get(self, request):
        session = request.session

        todo_items = session.get(settings.USER_TODO_SESSION_ID, None)
        if todo_items is None:
            todo_items = TodoItem.objects.filter(user=request.user).order_by('-create_time')

        return render(request, 'todo.html', {'todo_items' : todo_items})

    def post(self, request):
        title = request.POST.get('title', "Unknown")
        content = request.POST.get('content', '')
        user = request.user

        p = TodoItem.objects.create(title=title, content=content, user=user)

        session = request.session
        todo_items = session.get(settings.USER_TODO_SESSION_ID, None)
        if todo_items:
            todo_items.append(p)
            session.modified = True

        return redirect(reverse('todo:list'))

