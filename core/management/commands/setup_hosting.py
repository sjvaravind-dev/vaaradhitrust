from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Prepare the site on Hostinger: migrate, collectstatic, seed content."

    def handle(self, *args, **options):
        self.stdout.write("Running migrate...")
        call_command("migrate", interactive=False)
        self.stdout.write("Collecting static files...")
        call_command("collectstatic", interactive=False, verbosity=1)
        self.stdout.write("Seeding content...")
        call_command("seed_content")
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser("admin", "admin@vaaradhi.org.in", "ChangeMeNow123")
            self.stdout.write(
                self.style.WARNING(
                    "Created admin user admin / ChangeMeNow123 — change this password immediately."
                )
            )
        self.stdout.write(self.style.SUCCESS("Hosting setup complete."))
