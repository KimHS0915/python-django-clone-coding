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
    selected_country = request.GET.get('country', 'KR')
    selected_room_type = int(request.GET.get('room_type', 0))
    price = int(request.GET.get('price', 0))
    guests = int(request.GET.get('guests', 0))
    bedrooms = int(request.GET.get('bedrooms', 0))
    beds = int(request.GET.get('beds', 0))
    baths = int(request.GET.get('baths', 0))
    instant = request.GET.get('instant', False)
    super_host = request.GET.get('super_host', False)
    selected_amenities = request.GET.getlist('amenities')
    selected_facilities = request.GET.getlist('facilities')

    form = {
        'city': city,
        'selected_room_type': selected_room_type,
        'selected_country': selected_country,
        'price': price,
        'guests': guests,
        'bedrooms': bedrooms,
        'beds': beds,
        'baths': baths,
        'instant': instant,
        'super_host': super_host,
        'selected_amenities': selected_amenities,
        'selected_facilities': selected_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        'countries': countries,
        'room_types': room_types,
        'amenities': amenities,
        'facilities': facilities,
    }

    return render(request, "rooms/search.html", context={**form, **choices})
