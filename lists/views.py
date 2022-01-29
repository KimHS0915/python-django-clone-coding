from email import message
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext
from django.views.generic import TemplateView
from rooms.models import Room
from . import models


def toggle_room(request, room_pk):
    action = request.GET.get('action', None)
    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name='My Favourites Houses')
        if action == 'add':
            the_list.rooms.add(room)
            messages.success(request, gettext("Favourites added"))
        elif action == 'remove' or action == 'delete':
            the_list.rooms.remove(room)
            messages.success(request, gettext('Favourites removed'))
            if action == 'delete':
                return redirect(reverse('lists:see-favs'))
    return redirect(reverse('rooms:detail', kwargs={'pk': room_pk}))


class SeeFavouritesView(TemplateView):

    template_name = 'lists/list_detail.html'
