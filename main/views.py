from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from blog.models import Blog
from .models import Client, Mailing, Message, MailingLog
from .forms import ClientForm, MailingForm, MessageForm


class HomeView(TemplateView):
    template_name = 'main/home.html'
    extra_context = {
        'title': 'Главная страница',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_mailings_count = Mailing.objects.filter(status__in=['created', 'started']).count()
        context['active_mailings_count'] = active_mailings_count
        unique_clients_count = Client.objects.filter(is_active=True).distinct().count()
        context['unique_clients_count'] = unique_clients_count
        all_posts = list(Blog.objects.all())
        context['random_blog_posts'] = sample(all_posts, min(3, len(all_posts)))
        context['object_list'] = Mailing.objects.all()
        user = self.request.user
        user_group_names = [group.name for group in user.groups.all()]
        context['user_group_names'] = user_group_names
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:client_list')


class ClientListView(ListView):
    model = Client
    template_name = 'main/client_list.html'
    context_object_name = 'clients'


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/create_mailing.html'
    success_url = reverse_lazy('main:mailing')

    def form_valid(self, form):
        new_mailing = form.save()
        new_mailing.owner = self.request.user
        new_mailing.save()
        self.mailing_pk = new_mailing.pk
        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'main/mailing_detail.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(mailing=self.object)
        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing')

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.owner = self.request.user
            new_mailing.save()
        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'
    context_object_name = 'mailings'


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailing')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'main/create_message.html'
    success_url = reverse_lazy('main:mailing')
    context_object_name = 'messages'

    def form_valid(self, form):
        mailing_pk = self.kwargs['mailing_pk']
        mailing = get_object_or_404(Mailing, pk=mailing_pk)
        message = form.save(commit=False)
        message.mailing = mailing
        message.owner = self.request.user
        message.save()

        return redirect('main:mailing_detail', pk=mailing_pk)


class ReportView(ListView):
    model = MailingLog
    template_name = 'main/report.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return MailingLog.objects.filter(status='success')
