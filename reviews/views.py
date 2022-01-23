from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from rooms.models import Room
from . import forms, models


def create_review(request, room):
    if request.method == 'POST':
        form = forms.CreateReviewForm(request.POST)
        room = Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse('common:home'))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, 'Room reviewed')
            return redirect(reverse('rooms:detail', kwargs={'pk': room.pk}))


def delete_review(request, room, review):
    models.Review.objects.get_or_none(pk=review).delete()
    messages.success(request, 'Review deleted')
    return redirect(reverse('rooms:detail', kwargs={'pk': room}))
