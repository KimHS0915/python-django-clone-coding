from django import template
from django.shortcuts import redirect
from django.urls import reverse
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
        elif action == 'remove':
            the_list.rooms.remove(room)
    return redirect(reverse('rooms:detail', kwargs={'pk': room_pk}))


class SeeFavouritesView(TemplateView):

    template_name = 'lists/list_detail.html'
