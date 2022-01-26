from django.shortcuts import redirect
from django.urls import reverse
from rooms.models import Room
from . import models


def save_room(request, room_pk):
    room = Room.objects.get_or_none(pk=room_pk)
    if room is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name='My Favourites Houses')
        the_list.rooms.add(room)
    return redirect(reverse('rooms:detail', kwargs={'pk': room_pk}))
