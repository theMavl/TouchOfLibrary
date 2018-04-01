from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from library.forms import DeletePatron
from library.models import PatronInfo
from library.models import Reservation, GiveOut


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

            mail_subject = 'Touch of Library: Account deletion'
            message = render_to_string('mails/acc_delete_email.html', {
                'user': current_user,
                'reason': form.cleaned_data['reason'],
            })
            to_email = current_user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            current_user.is_active = False
            current_user.save()

            return HttpResponseRedirect('/library/patrons/')
    else:
        form = DeletePatron(initial={'comment': ''})
        return render(request, 'library/patron_delete.html',
                      context={'form': form,
                               'patron':current_patron})


