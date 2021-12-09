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
    instant = bool(request.GET.get('instant', False))
    superhost = bool(request.GET.get('superhost', False))
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
        'superhost': superhost,
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

    filter_args = {}

    if city:
        filter_args['city__startswith'] = city

    filter_args['country'] = selected_country

    if selected_room_type > 0:
        filter_args['room_type__pk__exact'] = selected_room_type

    if price > 0:
        filter_args['price__lte'] = price
    if guests > 0:
        filter_args['guests__gte'] = guests

    if bedrooms > 0:
        filter_args['bedrooms__gte'] = guests

    if beds > 0:
        filter_args['beds__gte'] = guests

    if baths > 0:
        filter_args['baths__gte'] = guests

    if instant:
        filter_args['instant_book'] = True

    if superhost:
        filter_args['host__superhost'] = True

    rooms = models.Room.objects.filter(**filter_args)

    if len(selected_amenities) > 0:
        for amenity in selected_amenities:
            rooms = rooms.filter(amenities__pk=int(amenity))

    if len(selected_facilities) > 0:
        for facility in selected_facilities:
            rooms = rooms.filter(facilities__pk=int(facility))

    return render(request, "rooms/search.html", context={**form, **choices, 'rooms': rooms})
