from django.urls import path

from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView
from . import views

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('detail/<pk>', BlogDetailView.as_view(), name='detail'),
    path('update/<pk>', BlogUpdateView.as_view(), name='update'),
    path('view/<pk>', BlogDetailView.as_view(), name='view'),
    path('delete/<pk>', BlogDeleteView.as_view(), name='delete'),

]
