from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, request, HttpResponseForbidden
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from library.forms import ImageUnsignedDirectForm, ImageDirectForm, DocImageForm
from library.logger import create_log
from library.models import Document, Author, DocType, Tag

import json
from cloudinary.forms import cl_init_js_callbacks
from cloudinary import api  # Only required for creating upload presets on the fly

from django.views.generic import ListView
from django.db.models import Q


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

    @method_decorator(permission_required('library.add_document'))
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentCreate, self).dispatch(request, *args, **kwargs)

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

    @method_decorator(permission_required('library.delete_document'))
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentDelete, self).dispatch(request, *args, **kwargs)

    success_url = reverse_lazy('document')


class DocumentUpdate(UpdateView):
    model = Document
    fields = 'title', 'authors', 'description', 'type', 'tags', 'bestseller', 'is_reference'
    template_name_suffix = '_update_form'

    @method_decorator(permission_required('library.change_document'))
    def dispatch(self, request, *args, **kwargs):
        return super(DocumentUpdate, self).dispatch(request, *args, **kwargs)

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


def upload(request):
    unsigned = request.GET.get("unsigned") == "true"

    if (unsigned):
        # For the sake of simplicity of the sample site, we generate the preset on the fly. It only needs to be created once, in advance.
        try:
            api.upload_preset(ImageUnsignedDirectForm.upload_preset_name)
        except api.NotFound:
            api.create_upload_preset(name=ImageUnsignedDirectForm.upload_preset_name, unsigned=True,
                                     folder="preset_folder")

    direct_form = ImageUnsignedDirectForm() if unsigned else ImageDirectForm()
    context = dict(
        # Form demonstrating backend upload
        backend_form=DocImageForm(),
        # Form demonstrating direct upload
        direct_form=direct_form,
        # Should the upload form be unsigned
        unsigned=unsigned,
    )
    # When using direct upload - the following call is necessary to update the
    # form's callback url
    cl_init_js_callbacks(context['direct_form'], request)

    instance = Document.objects.create()
    if request.method == 'POST':
        # Only backend upload should be posting here
        form = DocImageForm(request.POST, request.FILES, instance=instance)
        context['posted'] = form.instance
        if form.is_valid():
            # Uploads image and creates a model instance for it

            from library.logger import create_log
            create_log(request, "Created", instance)

            form.save()
            return redirect('document')
    instance.delete()
    return render(request, 'upload.html', context)


def direct_upload_complete(request):
    form = ImageDirectForm(request.POST)
    if form.is_valid():
        # Create a model instance for uploaded image using the provided data
        form.save()
        ret = dict(photo_id=form.instance.id)
    else:
        ret = dict(errors=form.errors)

    return HttpResponse(json.dumps(ret), content_type='application/json')


class SearchListView(ListView):
    model = Document

    def get_queryset(self):
        queryset = super(SearchListView, self).get_queryset()
        q = self.request.GET.get("q")

        if q:
            splitq = str(q).split()
            sor, sand = False, False
            if splitq.__contains__('AND'):
                sand = True
                splitq.remove('AND')
            if splitq.__contains__('OR'):
                sor = True
                splitq.remove('OR')
            if sor:
                return queryset.filter(
                    Q(title__icontains=splitq[0]) | Q(description__icontains=splitq[0]) | Q(
                        authors__first_name__icontains=splitq[0]) | Q(
                        authors__last_name__icontains=splitq[0]) | Q(title__icontains=splitq[1]) | Q(
                        description__icontains=splitq[1]) | Q(
                        authors__first_name__icontains=splitq[1]) | Q(
                        authors__last_name__icontains=splitq[1])).distinct().exclude(last_quantity__icontains=str(0))
            if sand:
                return queryset.filter(
                    (Q(title__icontains=splitq[0]) | Q(description__icontains=splitq[0]) | Q(
                        authors__first_name__icontains=splitq[0]) | Q(
                        authors__last_name__icontains=splitq[0])) & (
                            Q(title__icontains=splitq[1]) | Q(description__icontains=splitq[1]) | Q(
                        authors__first_name__icontains=splitq[1]) | Q(
                        authors__last_name__icontains=splitq[1]))).distinct().exclude(
                    last_quantity__icontains=str(0))

            return queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q) | Q(
                    authors__first_name__icontains=q) | Q(
                    authors__last_name__icontains=q)).distinct().exclude(last_quantity__icontains=str(0))

        return queryset
