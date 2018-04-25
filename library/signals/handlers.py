from library.logger import def_user_group, ContentType
from library.models import Log


def log_edit_document(sender, **kwargs):

    user = get_user_from_rec_stack()
    user_type = def_user_group(user)

    instance = kwargs["instance"]

    log = Log.objects.create(user=user,
                             user_type=user_type,
                             action="Changed",
                             object_content_type=ContentType.objects.get_for_model(instance.__class__),
                             object_id=instance.pk,
                             object_type=instance._meta.verbose_name,
                             object_name=instance.__str__(),
                             )
    log.save()


def log_delete_document(sender, **kwargs):

    user = get_user_from_rec_stack()
    user_type = def_user_group(user)

    instance = kwargs["instance"]

    log = Log.objects.create(user=user,
                             user_type=user_type,
                             action="Changed",
                             object_content_type=ContentType.objects.get_for_model(instance.__class__),
                             object_id=instance.pk,
                             object_type=instance._meta.verbose_name,
                             object_name=instance.__str__(),
                             )
    log.save()


def get_user_from_rec_stack():
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
        else:
            request = None
    return request.user