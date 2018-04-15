from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.contrib import auth

from library.forms import RenewDocumentForm
from library.models import GiveOut, PatronInfo, DocumentRequest

import datetime


def renew_document(request, id):
    user = auth.get_user(request)
    giveout = GiveOut.objects.get(id=id)
    if not user.has_perm("library.change_giveout") and user != giveout.user:
        return HttpResponseForbidden()

    document = giveout.document
    doc_instance = giveout.document_instance
    patron_user = giveout.user
    patron = PatronInfo.objects.get(user=patron_user)
    max_renew_times = patron.patron_type.max_renew_times
    outstanding_requests = DocumentRequest.objects.filter(document=document, outstanding=True)

    error_limit_of_renewals = False
    error_outstanding_request = False

    max_days = document.days_available(patron)

    if outstanding_requests:
        error_outstanding_request = True
    if giveout.renewed_times >= max_renew_times:
        error_limit_of_renewals = True

    if request.method == 'POST':

        form = RenewDocumentForm(request.POST)
        form.max_days = max_days
        form.error_limit_of_renewals = error_limit_of_renewals
        form.error_outstanding_request = error_outstanding_request
        form.return_date = doc_instance.due_back

        if form.is_valid():
            doc_instance.due_back = form.clean_due_date()
            giveout.renewed_times = giveout.renewed_times + 1
            doc_instance.save()
            giveout.save()
            return HttpResponseRedirect('/library/patrons/' + str(patron_user.id))

    else:
        proposed_renewal_date = doc_instance.due_back + datetime.timedelta(max_days)
        form = RenewDocumentForm(initial={
            "due_date": proposed_renewal_date,
        })

    return render(request, 'library/renew_details.html', context={'giveout': giveout,
                                                                  'patron_type': patron.patron_type,
                                                                  'form': form,
                                                                  'outstanding_requests': error_outstanding_request})
