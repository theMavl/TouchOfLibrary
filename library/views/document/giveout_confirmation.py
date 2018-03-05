import datetime

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from library.forms import DueDateForm
from library.models import PatronInfo, Reservation, GiveOut


@permission_required('library.add_giveout')
def giveout_confirmation(request, id):
    reservation = Reservation.objects.get(id=id)
    copy = reservation.document_copy
    patron = PatronInfo.objects.get(user_id=reservation.user.id)

    if patron.patron_type.privileges:
        max_days = copy.document.type.max_days_privileges
    else:
        if copy.document.bestseller:
            max_days = copy.document.type.max_days_bestseller

        else:
            max_days = copy.document.type.max_days
    if request.method == 'POST':

        form = DueDateForm(request.POST)
        form.max_days = max_days
        if form.is_valid():
            copy.due_back = form.clean_due_date()
            copy.document.quantity_synced = False
            copy.document.save()
            copy.status = 'g'
            copy.holder = reservation.user
            copy.save()
            GiveOut.objects.create(user=reservation.user, patron=patron, document=reservation.document,
                                   document_instance=copy)
            reservation.delete()
            return HttpResponseRedirect(reverse('reservation-list'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(max_days)
        form = DueDateForm(initial={"due_date": proposed_renewal_date,
                                    "max_date": max_days})

    return render(request, 'library/giveout_details.html',
                  context={'reservation': reservation,
                           'patron_type': patron.patron_type,
                           'form': form})
