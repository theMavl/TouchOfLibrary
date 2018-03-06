from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from library.forms import DeletePatron
from library.models import PatronInfo, Reservation, GiveOut
from django.core.mail import send_mail


@permission_required('auth.delete_user')
def delete_patron(request, pk):
    current_user = User.objects.get(id=pk)
    current_patron = PatronInfo.objects.get(user_id=pk)
    if request.method == 'POST':

        form = DeletePatron(request.POST)

        if form.is_valid():
            giveouts = GiveOut.objects.filter(user=current_user).all()
            if giveouts:
                return HttpResponseRedirect('/library/patrons/')

            reservations = Reservation.objects.filter(user=current_user).all()
            for r in reservations:
                r.document_copy.status = 'a'
                r.document.quantity_synced = False
                r.document_copy.save()
                r.document.save()
            current_user.delete()
            current_patron.delete()

            return HttpResponseRedirect('/library/patrons/')
    else:
        form = DeletePatron(initial={'comment': ''})
        return render(request, 'library/patron_delete.html',
                      context={'form': form,
                               'patron':current_patron})


