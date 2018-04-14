import json

from cloudinary.forms import cl_init_js_callbacks
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.forms import DocDirectForm
from library.models import Document, Author, DocType, Tag


class DocumentListView(generic.ListView):
    """
    page with all documents
    """
    model = Document
    paginate_by = 10


class AuthorsListView(generic.ListView):
    """
    page with all authors
    """
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """
    page with information about author
    """
    model = Author


class DocumentCreate(CreateView):
    model = Document
    fields = 'title', 'authors', 'description', 'type', 'tags', 'bestseller', 'is_reference'

    class Meta:
        model = Document
        fields = 'title', 'authors', 'description', 'type', 'tags', 'bestseller', 'is_reference'
        labels = {
            'title': 'Title',
            'authors': 'Authors',
            'description': 'Description',
            'type': 'Type',
            'tags': 'Tags',
            'bestseller': 'Bestseller',
            'is_reference': 'Is reference',
        }


class DocumentDelete(DeleteView):
    model = Document
    success_url = reverse_lazy('document')


class DocumentUpdate(UpdateView):
    model = Document
    fields = 'title', 'authors', 'description', 'type', 'tags', 'bestseller', 'is_reference'
    template_name_suffix = '_update_form'


class TypeListView(generic.ListView):
    """
    page with all DocTypes
    """
    model = DocType
    paginate_by = 10


class TypeDetailView(generic.DetailView):
    """
    page with information about DocType
    """
    model = DocType


class TagListView(generic.ListView):
    """
    page with all Tags
    """
    model = Tag
    paginate_by = 10


def upload_prompt(request, pk):
    context = dict(direct_form=DocDirectForm())
    cl_init_js_callbacks(context['direct_form'], request)
    return render(request, 'upload_prompt.html', context)


@csrf_exempt
def direct_upload_complete(request):
    form = DocDirectForm(request.POST)
    if form.is_valid():
        form.save()
        ret = dict(doc_id=form.instance.id)
    else:
        ret = dict(errors=form.errors)

    return HttpResponse(json.dumps(ret), content_type='application/json')
