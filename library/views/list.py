from django.contrib import auth
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect

from library.models import User, Reservation, GiveOut


@permission_required('library.change_reservation')
def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'library/reservation_list.html', context={'reservations': reservations})


@permission_required('library.change_patron')
def patrons_list(request):
    user = auth.get_user(request)
    if not user.has_perm('library.change_patron'):
        return redirect('dashboard')
    if user.has_perm("library.change_user"):
        record = User.objects.all()
    else:
        record = User.objects.filter(is_patron=True)
    return render(request, 'library/patrons_list.html', context={'patrons': record})

@permission_required('library.change_giveout')
def giveout_list(request):
    giveouts = GiveOut.objects.all()
    return render(request, 'library/giveout_list.html', context={'giveouts': giveouts})
