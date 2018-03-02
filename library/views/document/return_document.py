from django.contrib.auth.decorators import permission_required
from library.models import PatronInfo, GiveOut
from django.shortcuts import render, redirect
from library.forms import ReturnDocumentForm


@permission_required('library.delete_giveout')
def return_document(request, id):
    giveout = GiveOut.objects.get(id=id)
    copy = giveout.document_instance
    document = giveout.document
    patron_user = giveout.user
    patron_type = PatronInfo.objects.filter(user=patron_user)
    if patron_type:
        patron_type = patron_type.first().patron_type
    else:
        patron_type = None

    if request.method == 'POST':

        form = ReturnDocumentForm(request.POST)

        if form.is_valid():
            copy.status = 'a'
            copy.holder = None
            document.quantity_synced = False
            copy.save()
            document.save()
            giveout.delete()
            return redirect('patron-details', id=patron_user.id)
    else:
        form = ReturnDocumentForm(initial={"librarian_confirm": False})

    return render(request, 'library/document_return.html',
                  context={'giveout': giveout, 'patron_type': patron_type, 'overdue_days': 0, 'fine': 0.0,
                           'form': form})