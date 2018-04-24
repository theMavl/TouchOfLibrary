from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth

from library.forms import DeletePatron
from library.models import User
from library.models import Reservation, GiveOut


@permission_required('library.change_patron')
def delete_patron(request, pk):
    user = auth.get_user(request)
    user_to_delete = User.objects.get(id=pk)

    # User of lower rank can not delete user of higher rank
    user_rank = 0
    user_to_delete_rank = 0

    if user.has_perm("library.change_user"):
        user_rank += 1
    if user_to_delete.has_perm("library.change_user"):
        user_to_delete_rank += 1

    if user.is_staff:
        user_rank = 100
    if user_to_delete.is_staff:
        user_to_delete_rank = 100

    if user.is_superuser:
        user_rank = 999
    if user_to_delete.is_superuser:
        user_to_delete_rank = 999

    if request.method == 'POST':

        form = DeletePatron(request.POST)

        if form.is_valid():
            if (not user_to_delete.is_patron and not user.has_perm("library.change_user")) or \
                    (user_rank < user_to_delete_rank):
                return HttpResponse("This action is forbidden!")

            giveouts = GiveOut.objects.filter(user=user_to_delete).all()
            if giveouts:
                return HttpResponseRedirect('/library/patrons/')

            reservations = Reservation.objects.filter(user=user_to_delete).all()
            for r in reservations:
                r.document_copy.status = 'a'
                r.document.quantity_synced = False
                r.document_copy.save()
                r.document.save()

            message = render_to_string('mails/acc_delete_email.html', {
                'user': user_to_delete,
                'reason': form.cleaned_data['reason'],
            })
            user_to_delete.email_user('Touch of Library: Account deletion', message)

            from library.logger import create_log
            create_log(request, "Disabled", user_to_delete)

            user_to_delete.is_active = False
            user_to_delete.save()

            return HttpResponseRedirect('/library/patrons/')
    else:
        form = DeletePatron(initial={'comment': ''})
        return render(request, 'library/patron_delete.html',
                      context={'form': form,
                               'patron': user_to_delete})
