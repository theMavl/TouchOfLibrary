from django.contrib.auth.decorators import permission_required
from library.models import GiveOut, GiveOutLogEntry
from django.shortcuts import render, redirect
from library.forms import ReturnDocumentForm


@permission_required('library.delete_giveout')
def return_document(request, id):
    giveout = GiveOut.objects.get(id=id)
    copy = giveout.document_instance
    document = giveout.document
    patron_user = giveout.user
    patron_type = patron_user.patron_type

    if request.method == 'POST':

        form = ReturnDocumentForm(request.POST)

        if form.is_valid():
            GiveOutLogEntry.objects.create(timestamp_given_out=giveout.timestamp, timestamp_due_back=copy.due_back,
                                           user=copy.holder, patron_information=patron_user,
                                           document_instance_summary=copy.summary())
            copy.clean_giveout(request)

            from library.logger import create_log
            create_log(request, "Accepted Return", copy)

            giveout.delete()
            return redirect('patron-details', id=patron_user.id)
    else:
        form = ReturnDocumentForm(initial={"librarian_confirm": False})

    return render(request, 'library/document_return.html',
                  context={'giveout': giveout, 'patron_type': patron_type,
                           'overdue_days': giveout.document_instance.overdue_days(),
                           'fine': giveout.document_instance.fine(),
                           'form': form})
