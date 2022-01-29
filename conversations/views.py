from pipes import Template
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from users.models import User
from . import models


def go_conversation(request, host_pk, guest_pk):
    host = User.objects.get_or_none(pk=host_pk)
    guest = User.objects.get_or_none(pk=guest_pk)
    if host is not None and guest is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=host) & Q(participants=guest)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(host, guest)
        return redirect(reverse('conversations:detail', kwargs={'pk': conversation.pk}))


class ConversationDetailView(DetailView):

    model = models.Conversation
    template_name = 'conversations/detail.html'
