from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Picture(models.Model):
    title = models.CharField(max_length=100, blank=True, default='Unknown')
    #image = models.ImageField(upload_to=settings.IMAGE_DIR)
    image_url = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pic_upload:pic_detail', args=[str(self.id)])

    class Meta:
        db_table = 'picture'
        ordering =  ['-date']