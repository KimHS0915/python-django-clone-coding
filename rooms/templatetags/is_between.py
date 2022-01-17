import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def is_between(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(
            year=day.year, month=day.month, day=day.number)
        reservation_models.BetweenDay.objects.get(
            day=date, reservation__room=room)
        return True
    except reservation_models.BetweenDay.DoesNotExist:
        return False
