from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content',)
    success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs.get('pk')])


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview_img')
    success_url = reverse_lazy('blog:list')


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.views_count += 1
        post.save()
        return super().get(request, *args, **kwargs)


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)
