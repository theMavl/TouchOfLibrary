from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from library.models import User, Reservation, GiveOut, GiveOutLogEntry, DocumentRequest


@login_required
def patron_details(request, id):
    user = auth.get_user(request)

    if not user.has_perm('library.change_patron'):
        return redirect('dashboard')

    patron_user = User.objects.get(id=id)
    reservation_list = Reservation.objects.filter(user_id=patron_user.id)
    giveout_list = GiveOut.objects.filter(user_id=patron_user.id)
    giveout_log_list = GiveOutLogEntry.objects.filter(user_id=patron_user.id)
    request_list = DocumentRequest.objects.filter(user_id=patron_user.id)

    return render(
        request,
        'library/patron_detail.html',
        context={'patron_user': patron_user,
                 'reservation_table': reservation_list,
                 'giveout_table': giveout_list,
                 'giveout_log_table': giveout_log_list,
                 'request_table': request_list},
    )
