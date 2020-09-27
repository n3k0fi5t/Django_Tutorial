from django.shortcuts import render, redirect, reverse
from django.views import View

from .models import CrawlTask
from .forms import TaskForm

from .tasks import create_crawl_task, crawler_init
from .tasks import m

# Create your views here.
class TaskBoard(View):
    def get(self, request):
        if m is None:
            crawler_init()

        # pagination
        task_list = CrawlTask.objects.all()
        return render(request, 'crawler_status.html', {'task_list' : task_list })

class TaskSubmit(View):
    def get(self, request, form=None):
        return render(request, 'crawler_submit.html')

    def post(self, request):
        form = TaskForm(request.POST)

        if form.is_valid():
            success = create_crawl_task(form.cleaned_data['url'])
            return redirect(reverse('crawler:status'))
        else:
            return render(request, 'crawler_submit.html', {'form':form})
