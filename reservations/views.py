import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from rooms.models import Room
from . import models


class CreateError(Exception):
    pass


def create_reservation(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = Room.objects.get(pk=room)
        models.BetweenDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse('common:home'))
    except models.BetweenDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse('common:home'))
