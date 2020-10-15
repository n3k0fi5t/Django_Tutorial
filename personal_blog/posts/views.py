from django.shortcuts import render, reverse, get_object_or_404
from django.shortcuts import HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator

from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify

from .models import Post
from .forms import PostForm

# Create your views here.
class PostCreateView(View):
    def get(self, request):
        form = PostForm()
        context = {
            'form' : form,
        }
        return render(request, 'post_form.html', context)

    @method_decorator(login_required)
    def post(self, request):
        form = PostForm(self.request.POST or None, self.request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            # message success
            messages.success(request, "Create successfully")
            return HttpResponseRedirect(instance.get_absolute_url())

        form = PostForm()
        context = {
            'form' : form
        }
        return render(request, 'post_form.html', context)

class PostUpdateView(View):
    def get(self, request, id):
        instance = get_object_or_404(Post, id=id)
        form = PostForm(instance=instance)
        context = {
            'form' : form,
        }
        return render(request, 'post_form.html', context)

    def post(self, request, id):
        instance = get_object_or_404(Post, id=id)
        form = PostForm(self.request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, "Update successfully")
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            context = {
                'form' : form,
            }
            return render(request, 'post_form.html', context)



class PostDeleteView(View):
    def get(self, request, id=None):
        instance = get_object_or_404(Post, id=id)
        instance.delete()

        messages.success(request, "Delete succefully")
        return redirect(reverse('posts:list'))


class PostDetailView(View):
    def get(self, request, id):
        instance = get_object_or_404(Post, id=id)
        context = {
            'instance' : instance,
            'title' : instance.title,
        }
        return render(request, 'post_detail.html', context)

def paginate_post(request, query_set):
    paginator = Paginator(query_set, 3) # Show 3 contacts per page.
    page_request_var = 'page'
    page_number = request.GET.get(page_request_var)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj,
        'page_request_var' : page_request_var,
        'title' : 'List'
    }
    return render(request, 'post_list.html', context)


class PostListView(View):
    def get(self, request):
        post_list = Post.objects.all()

        query = request.GET.get('query')
        if query:
            post_list = Post.objects.all().filter(
                Q(content__contains=query) |
                Q(title__contains=query)
            ).distinct() # make it distinct
        else:
            post_list = Post.objects.all()

        return paginate_post(request, post_list)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exist = qs.exists()
    if exist:
        slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=slug)
    return slug

def pre_save_post_signal_receiver(sender, instance, *args, **kargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_signal_receiver, sender=Post)