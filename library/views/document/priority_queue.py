from django.shortcuts import render

from library.models import DocumentRequest, Document


def get_priority_queue(request, id):
    document = Document.objects.filter(id=id)
    requests = DocumentRequest.objects.filter(document_id=id)
    importanse = []

    for rec in requests:
        importanse.append(rec.importance())
    queue = sorted(zip(requests, importanse), key=lambda t: t[1], reverse=True)
    return render(request, "library/priority_queue.html", context={'queue': queue,
                                                                   'document': document})
