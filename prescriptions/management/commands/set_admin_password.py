from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Sets the password for the admin user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin = User.objects.get(username='admin')
        admin.set_password('admin123')
        admin.save()
        self.stdout.write(self.style.SUCCESS('Successfully set admin password'))