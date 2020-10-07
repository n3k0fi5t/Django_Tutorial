from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import View

# Create your views here.
class PostCreateView(View):
    def get(self, request):
        return render(request, 'index.html')

class PostUpdateView(View):
    def get(self, request):
        return render(request, 'index.html')

class PostDeleteView(View):
    def get(self, request):
        return render(request, 'index.html')

class PostDetailView(View):
    def get(self, request):
        return render(request, 'index.html')

class PostListView(View):
    def get(self, request):
        return render(request, 'index.html')

