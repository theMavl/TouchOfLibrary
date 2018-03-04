from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.models import Document, Author


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
    fields = 'title', 'authors', 'description', 'type', 'tags', 'bestseller', 'is_reference',


class DocumentDelete(DeleteView):
    model = Document
    success_url = reverse_lazy('document')


class DocumentUpdate(UpdateView):
    model = Document
    fields = 'title', 'authors', 'description', 'type', 'tags', 'bestseller', 'is_reference'
    template_name_suffix = '_update_form'
