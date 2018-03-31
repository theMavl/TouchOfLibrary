from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from library.models import DocumentRequest
from django.http import HttpResponseRedirect


@permission_required("library.change_documentrequest")
@permission_required("library.edit_documentrequest")
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
