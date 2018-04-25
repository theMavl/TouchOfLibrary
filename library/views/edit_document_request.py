from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from library.models import DocumentRequest, GiveOut
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@permission_required("library.change_documentrequest")
def edit_document_request(request, id, action):
    return_user_id = -1
    if action == 'outstanding':
        current_request = DocumentRequest.objects.filter(id=id)
        if current_request:
            current_request = current_request.first()
            return_user_id = current_request.user_id
            if current_request.outstanding:
                current_request.outstanding = False
                current_request.save()

                from library.logger import create_log
                create_log(request, "Removed Outstanding Request", current_request.document)

            else:
                outstanding_requests = DocumentRequest.objects.filter(document_id=current_request.document_id, outstanding=True)
                if not outstanding_requests:
                    current_request.outstanding = True
                    current_request.save()

                    from library.logger import create_log
                    create_log(request, "Created Outstanding Request", current_request.document)

                    giveouts = GiveOut.objects.filter(document=current_request.document)
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
        current_request = DocumentRequest.objects.filter(id=id)
        if current_request:

            current_request = current_request.first()
            return_user_id = current_request.user_id

            from library.logger import create_log
            create_log(request, "Removed Request", current_request.document)

            current_request.delete()
    if return_user_id == -1:
        return redirect('patrons-list')
    else:
        return redirect('patron-details', id=return_user_id)
