from email import message
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from users.models import User
from . import models, forms


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


class ConversationDetailView(View):

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        form = forms.AddCommentForm()
        return render(
            self.request,
            'conversations/detail.html',
            {'conversation': conversation, 'form': form}
        )

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        form = forms.AddCommentForm(self.request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            if message is not None:
                models.Message.objects.create(
                    message=message, user=self.request.user, conversation=conversation)
        return redirect(reverse('conversations:detail', kwargs={'pk': pk}))
