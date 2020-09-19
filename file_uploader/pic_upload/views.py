from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from django.views import View
from django.conf import settings
from django.utils.crypto import get_random_string

from .models import Picture
from .form import ImageUploadForm

import os
import hashlib

def generate_image_name(title):
    salt = get_random_string(10)
    data = bytes(title + salt, 'utf-8')
    
    return str(hashlib.sha256(data).hexdigest())


class PictureUpload(View):
    def get(self, request):
        form = ImageUploadForm()

        return render(request, 'picture_upload.html', {'form' : form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            img = form.cleaned_data['image']

            suffix = os.path.splitext(img.name)[-1].lower()
            name = generate_image_name(title) + suffix
            with open(os.path.join(settings.IMAGE_UPLOAD_DIR, name), 'wb') as f:
                for chunk in img:
                    f.write(chunk)

            p = Picture.objects.create(title=title, image_url=f"{settings.IMAGE_URL_PREFIX}/{name}")
            
            return redirect(reverse('pic_upload:pic_detail', args=[str(p.id)]))
        else:
            return redirect(reverse('pic_upload:pic_upload'))

class PictureDetail(View):
    def get(self, request, id):
        picture = Picture.objects.get(id=id)

        return render(request, 'picture_detail.html', {'picture' : picture})

class PictureList(View):
    def get(self, request):
        picture_list = Picture.objects.all()

        return render(request, 'picture_list.html', {'picture_list' : picture_list})

# Create your views here.
class PicList(ListView):
    queryset = Picture.objects.all().order_by('-date')

    context_object_name = 'latest_picture_list'

    template_name = "picture_list.html"

class PicDetail(DetailView):
    model = Picture

    template_name = "picture_detail.html"

class PicUpload(CreateView):
    model = Picture

    fields = ['title', 'image']

    template_name = "picture_upload.html"