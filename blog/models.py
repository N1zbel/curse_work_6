from django.conf import settings
from django.db import models
from pytils.translit import slugify

from main.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.CharField(max_length=150, unique=True, verbose_name='slug')
    content = models.TextField(verbose_name='Содержимое')
    preview_img = models.ImageField(upload_to='blog/images/', verbose_name='Превью', **NULLABLE)
    date_of_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
