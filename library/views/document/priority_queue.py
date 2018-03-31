from django.shortcuts import render

from library.models import DocumentRequest, Document


def get_priority_queue(request, id):
    document = Document.objects.filter(id=id).first()
    requests = DocumentRequest.objects.filter(document_id=id)
    importance = []

    for rec in requests:
        importance.append(rec.importance())
    queue = sorted(zip(requests, importance), key=lambda t: t[1], reverse=True)
    return render(request, "library/priority_queue.html", context={'queue': queue,
                                                                   'document': document})
