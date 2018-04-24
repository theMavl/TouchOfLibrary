from django.shortcuts import render, get_object_or_404

from library.forms import RequestAllConfirm
from library.models import DocumentRequest, Document, User, GiveOut
from django.contrib.auth.decorators import permission_required
from django.contrib import auth


@permission_required("library.change_documentrequest")
def get_priority_queue(request, id):
    document = Document.objects.filter(id=id).first()
    requests = DocumentRequest.objects.filter(document_id=id)
    importance = []

    for rec in requests:
        importance.append(rec.importance())
    queue = sorted(zip(requests, importance), key=lambda t: t[1], reverse=True)
    return render(request, "library/priority_queue.html", context={'queue': queue,
                                                                   'document': document})


@permission_required("library.change_documentrequest")
def request_all(request, id, reason):
    requests = DocumentRequest.objects.filter(document_id=id)
    document = get_object_or_404(Document, id=id)
    giveouts = GiveOut.objects.filter(document=document)
    user = auth.get_user(request)

    document.is_reference = True

    from django.core.mail import send_mail
    for rec in giveouts:
        send_mail("Document Return", "You need to return a document [" + str(document.title) + "] because of " + str(reason),
                  User.objects.get(user.pk).email, [rec.user.email])
        print("Email is sent to [" + str(User.objects.get(user.pk).email) + "]")
        pass

    for rec in requests:
        rec.delete()

    document.save()


@permission_required('library.change_documentrequest')
def request_all_view(request, pk):
    if request.method == 'POST':
        form = RequestAllConfirm(request.POST)

        if form.is_valid():
            request_all(request, pk, form.cleaned_data['reason'])

            document = get_object_or_404(Document, id=pk)
            from library.logger import create_log
            create_log(request, "Requested All copies", document)

            from django.http import HttpResponseRedirect
            return HttpResponseRedirect('/library/document/' + str(pk))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RequestAllConfirm(initial={
            'librarian_confirmation': False,
            'reason': '',
        })

    return render(request, 'library/request_all.html', {'form': form, 'userid': pk})
