from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from library.models import DocumentRequest, GiveOut
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@permission_required("library.change_documentrequest")
def edit_document_request(request, id, action):
    return_user_id = -1
    if action == 'outstanding':
        request = DocumentRequest.objects.filter(id=id)
        if request:
            request = request.first()
            return_user_id = request.user_id
            if request.outstanding:
                request.outstanding = False
                request.save()
            else:
                outstanding_requests = DocumentRequest.objects.filter(document_id=request.document_id, outstanding=True)
                if not outstanding_requests:
                    request.outstanding = True
                    request.save()
                    giveouts = GiveOut.objects.filter(document=request.document)
                    for x in giveouts:
                        mail_subject = 'Touch of Library: Please return document'
                        message = render_to_string('mails/return_request.html', {
                            'document': x.document_instance.summary(),
                            'user': x.user,
                        })
                        to_email = x.user.email
                        email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
                        email.attach_alternative(message, "text/html")
                        email.send()
    elif action == 'delete':
        request = DocumentRequest.objects.filter(id=id)
        if request:
            request = request.first()
            return_user_id = request.user_id
            request.delete()
    if return_user_id == -1:
        return redirect('patrons-list')
    else:
        return redirect('patron-details', id=return_user_id)
