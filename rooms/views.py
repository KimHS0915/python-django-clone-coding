from django.utils import timezone
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django_countries import countries
from . import models


class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 3
    ordering = 'created'
    context_object_name = 'rooms'
    template_name = 'rooms/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['now'] = now
        return context


class RoomDetailView(DetailView):
    """ Room Detail Definition """

    model = models.Room


def search(request):
    city = request.GET.get('city')
    city = city.capitalize() if city else ''
    room_types = models.RoomType.objects.all()
    return render(request, "rooms/search.html", context={
        'city': city,
        'countries': countries,
        'room_types': room_types,
    })
