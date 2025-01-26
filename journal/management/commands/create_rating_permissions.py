from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group
from journal.models import Rating

class Command(BaseCommand):
    help = 'Creates the Rating permissions and Judge group'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Rating)

        add_rating_permission, created_add = Permission.objects.get_or_create(
            codename='add_rating',
            name='Can add rating',
            content_type=content_type
        )
        change_rating_permission, created_change = Permission.objects.get_or_create(
            codename='change_rating',
            name='Can change rating',
            content_type=content_type
        )
        delete_rating_permission, created_delete = Permission.objects.get_or_create(
            codename='delete_rating',
            name='Can delete rating',
            content_type=content_type
        )

        judges_group, created_group = Group.objects.get_or_create(name='Judges')
        if created_group:
            judges_group.permissions.add(add_rating_permission, change_rating_permission, delete_rating_permission)
            self.stdout.write(self.style.SUCCESS('Judges group created and permissions added'))
        else:
            self.stdout.write(self.style.SUCCESS('Judges group already exists.'))
        if created_add:
            self.stdout.write(self.style.SUCCESS('add_rating permission created.'))
        else:
            self.stdout.write(self.style.SUCCESS('add_rating permission already exists.'))
        if created_change:
            self.stdout.write(self.style.SUCCESS('change_rating permission created.'))
        else:
            self.stdout.write(self.style.SUCCESS('change_rating permission already exists.'))
        if created_delete:
            self.stdout.write(self.style.SUCCESS('delete_rating permission created.'))
        else:
            self.stdout.write(self.style.SUCCESS('delete_rating permission already exists.'))