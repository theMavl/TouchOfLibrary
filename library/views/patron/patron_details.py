from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from library.models import PatronInfo, Reservation, GiveOut


@login_required
def patron_details(request, id):
    user = auth.get_user(request)

    if not user.has_perm('auth.change_user'):
        return redirect('dashboard')

    patron_user = User.objects.get(id=id)
    patron = PatronInfo.objects.get(user_id=patron_user.id)
    reservation_list = Reservation.objects.filter(user_id=patron_user.id)
    giveout_list = GiveOut.objects.filter(user_id=patron_user.id)

    return render(
        request,
        'library/patron_detail.html',
        context={'patron_user': patron_user,
                 'patron_info': patron,
                 'reservation_table': reservation_list,
                 'giveout_table': giveout_list},
    )

