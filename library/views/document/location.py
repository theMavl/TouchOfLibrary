from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView

from library.forms import LocationCreate, LocationUpdate, DocumentInstance
from library.models import LibraryLocation
from library.views import generic


class LocationListView(generic.ListView):
    model = LibraryLocation

@permission_required('library.change_author')
def location_update(request, id):
    instance = get_object_or_404(LibraryLocation, id=id)
    form = LocationUpdate(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('location_list')
    return render(request, 'library/location_update.html', {'form': form})


@permission_required('delete.create_author')
def location_delete_confirmation(request, id):
    instance = get_object_or_404(LibraryLocation, id=id)
    documents = DocumentInstance.objects.filter(location__room=instance.room, location__level=instance.level)
    return render(request, 'library/location_deleteconfirm.html', {'instance': instance, 'id': id, 'documents': documents})


@permission_required('delete.create_author')
def location_delete(request, id):
        instance = get_object_or_404(LibraryLocation, id=id)
        instance.delete()
        return redirect('location_list')


@permission_required('library.add_author')
def create_location(request):
        form = LocationCreate(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('location_list')
        return render(request, 'library/location_create.html', {'form': form})
