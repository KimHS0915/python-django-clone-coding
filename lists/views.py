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
    return_addr = reverse('common:home')
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name='My Favourites Houses')
        if action == 'add':
            the_list.rooms.add(room)
            messages.success(request, gettext("Favourites added"))
        elif action == 'remove':
            the_list.rooms.remove(room)
            messages.success(request, gettext('Favourites removed'))
        elif action == 'add1':
            the_list.rooms.add(room)
            messages.success(request, gettext("Favourites added"))
            return_addr = reverse('rooms:detail', kwargs={'pk': room_pk})
        elif action == 'remove1':
            the_list.rooms.remove(room)
            messages.success(request, gettext('Favourites removed'))
            return_addr = reverse('rooms:detail', kwargs={'pk': room_pk})
        elif action == 'add2':
            the_list.rooms.add(room)
            messages.success(request, gettext("Favourites added"))
            return_addr = reverse('lists:see-favs')
        elif action == 'remove2':
            the_list.rooms.remove(room)
            messages.success(request, gettext('Favourites removed'))
            return_addr = reverse('lists:see-favs')
    return redirect(return_addr)


class SeeFavouritesView(TemplateView):

    template_name = 'lists/list_detail.html'
