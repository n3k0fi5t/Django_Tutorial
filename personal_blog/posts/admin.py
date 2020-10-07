from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'timestamp']
    list_display_links = ['title']
    list_filter = ['updated']
    search_fields = ['content']

    class Meta:
        Post

# Register your models here.