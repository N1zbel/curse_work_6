from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    ClientCreateView, ClientUpdateView, ClientListView, ClientDeleteView,
    MailingCreateView, MailingUpdateView, MailingListView, MailingDeleteView, MailingDetailView,
    MessageCreateView, HomeView, ReportView,
)

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mailing/', MailingListView.as_view(), name='mailing'),
    path('mailing/create/', MailingCreateView.as_view(), name='create'),
    path('mailing/<pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing/delete/<pk>', MailingDeleteView.as_view(), name='delete'),
    path('mailing/update/<pk>', MailingUpdateView.as_view(), name='update'),
    path('mailing/create_message/<mailing_pk>', MessageCreateView.as_view(), name='create_message'),
    path('client/update/<pk>', ClientUpdateView.as_view(), name='client_update'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/delete/<pk>', ClientDeleteView.as_view(), name='client_delete'),
    path('report/',  cache_page(60)(ReportView.as_view()), name='report'),

    ]