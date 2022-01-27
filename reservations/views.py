import datetime
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import View
from rooms.models import Room
from reviews.forms import CreateReviewForm
from . import models


class CreateError(Exception):
    pass


def create_reservation(request, room, year, month, day):

    if request.user.is_authenticated == False:
        messages.error(request, _("Login required"))
        return redirect(reverse('users:login'))
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = Room.objects.get(pk=room)
        models.BetweenDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (Room.DoesNotExist, CreateError):
        messages.error(request, _("Can't Reserve That Room"))
        return redirect(reverse('common:home'))
    except models.BetweenDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse('reservations:detail', kwargs={'pk': reservation.pk}))


class ReservationDetailView(View):

    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = CreateReviewForm()
        return render(
            self.request,
            'reservations/detail.html',
            {
                'reservation': reservation,
                'form': form,
            },
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user
        and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == 'confirm':
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == 'cancel':
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BetweenDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, _('Reservation Updated'))
    return redirect(reverse('reservations:detail', kwargs={'pk': reservation.pk}))
