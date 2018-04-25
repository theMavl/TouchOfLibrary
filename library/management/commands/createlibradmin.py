from django.core.management.base import BaseCommand, CommandError
from library.models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Creates new administrator'

    def handle(self, *args, **options):
        if User.objects.filter(groups__name='Administrator'):
            self.stdout.write(self.style.ERROR('Administrator already exists!'))
        else:
            group_admin = Group.objects.get(name="Administrator")
            libradmin = User.objects.create_user(username='libradmin', email='libradmin@touchoflibrary.com',
                                                 password='cakeisalie',
                                                 first_name='John', last_name='Smith', phone_number='30000',
                                                 address='Hidden', telegram='Hidden', is_patron=False)
            libradmin.groups.add(group_admin)
            self.stdout.write(self.style.SUCCESS("Successfully created admin 'libradmin'"))