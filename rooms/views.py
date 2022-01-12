from django.contrib.messages.api import success
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 3
    ordering = 'created'
    context_object_name = 'rooms'
    template_name = 'rooms/home.html'


class RoomDetailView(DetailView):
    """ Room Detail Definition """

    model = models.Room


class SearchView(View):
    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get('country')

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                room_type = form.cleaned_data.get('room_type')
                price = form.cleaned_data.get('price')
                guests = form.cleaned_data.get('guests')
                bedrooms = form.cleaned_data.get('bedrooms')
                beds = form.cleaned_data.get('beds')
                baths = form.cleaned_data.get('baths')
                instant_book = form.cleaned_data.get('instant_book')
                superhost = form.cleaned_data.get('superhos')
                amenities = form.cleaned_data.get('amenities')
                facilities = form.cleaned_data.get('facilities')

                filter_args = {}

                if city:
                    filter_args['city__startswith'] = city

                filter_args['country'] = country

                if room_type:
                    filter_args['room_type'] = room_type

                if price:
                    filter_args['price__lte'] = price

                if guests:
                    filter_args['guests__gte'] = guests

                if bedrooms:
                    filter_args['bedrooms__gte'] = guests

                if beds:
                    filter_args['beds__gte'] = guests

                if baths:
                    filter_args['baths__gte'] = guests

                if instant_book:
                    filter_args['instant_book'] = True

                if superhost:
                    filter_args['host__superhost'] = True

                qs = models.Room.objects.filter(
                    **filter_args).order_by('-created')

                for amenity in amenities:
                    qs = qs.filter(amenities=amenity)

                for facility in facilities:
                    qs = qs.filter(facilities=facility)

                page = request.GET.get('page')
                paginator = Paginator(qs, 5, orphans=5)
                rooms = paginator.get_page(page)
                path = request.get_full_path().split(
                    '&page=')[0].replace('/rooms/search/?', '')

                return render(request, "rooms/search.html", context={
                    'form': form, 'rooms': rooms, 'path': path})
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", context={'form': form})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = 'rooms/room_edit.html'
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = 'rooms/room_photos.html'

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        photo = models.Photo.objects.get(pk=photo_pk)
        if room.host.pk != user.pk and user.pk != photo.room.pk:
            messages.error(request, "Can't delete that photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, 'Photo deleted')
        return redirect(reverse('rooms:photos', kwargs={'pk': room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse('common:home'))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = 'rooms/photo_edit.html'
    pk_url_kwarg = 'photo_pk'
    fields = ('caption',)

    def get_success_url(self):
        room_pk = self.kwargs.get('room_pk')
        return reverse('rooms:photos', kwargs={'pk': room_pk})

    def get_object(self, queryset=None):
        photo = super().get_object(queryset=queryset)
        if photo.room.host.pk != self.request.user.pk:
            raise Http404()
        return photo


class AddPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, FormView):

    model = models.Photo
    template_name = 'rooms/photo_create.html'
    fields = (
        'caption',
        'file',
    )
    form_class = forms.CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        form.save(pk)
        messages.success(self.request, 'Photo Uploaded')
        return redirect(reverse('rooms:photos', kwargs={'pk': pk}))
