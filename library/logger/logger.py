from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.contrib import auth
from library.models import User, Document, DocumentInstance, Author, LibraryLocation, DocType, Tag, Log


def create_log(request, action, some_class: Model):
    user = auth.get_user(request)
    user_type = def_user_group(user)
    message = action

    # reference = None
    # detailed = False
    #
    # if isinstance(some_class, User):
    #     reference = 'patron-details'
    #     detailed = True
    # elif isinstance(some_class, Document):
    #     reference = 'document-detail'
    #     detailed = True
    # elif isinstance(some_class, DocumentInstance):
    #     reference = 'document-detail'
    #     detailed = True
    # elif isinstance(some_class, Author):
    #     reference = 'author-detail'
    #     detailed = True
    # elif isinstance(some_class, LibraryLocation):
    #     reference = 'location_list'
    #     detailed = True
    # elif isinstance(some_class, DocType):
    #     reference = 'types-detail'
    #     detailed = True
    # elif isinstance(some_class, Tag):
    #     reference = 'tags-detail'
    #     detailed = False

    log = Log.objects.create(user=user,
                             user_type=user_type,
                             action=message,
                             object_content_type=ContentType.objects.get_for_model(some_class.__class__),
                             object_id=some_class.pk,
                             object_type=some_class._meta.verbose_name,
                             object_name=some_class.__str__(),
                             )
    log.save()


def def_user_group(user):
    if user.is_patron:
        return "Patron"
    elif user.is_superuser:
        return "Admin"
    else:
        return "Librarian"
