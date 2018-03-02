from django.contrib import auth
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect

from library.models import PatronInfo, Reservation, GiveOut


@permission_required('library.change_reservation')
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'library/reservation_list.html', context={'reservations': reservations})


@permission_required('auth.change_user')
def patrons_list(request):
    user = auth.get_user(request)
    if not user.has_perm('auth.change_user'):
        return redirect('dashboard')

    record = PatronInfo.objects.all()
    return render(request, 'library/patrons_list.html', context={'patrons': record})


@permission_required('library.change_giveout')
def giveout_list(request):
    giveouts = GiveOut.objects.all()
    return render(request, 'library/giveout_list.html', context={'giveouts': giveouts})