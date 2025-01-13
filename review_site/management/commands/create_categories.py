from django.core.management import BaseCommand

from ...models import Category


class Command(BaseCommand):
    """Створення котегорій"""
    help = "Створення записів для моделі категорій"

    def handle(self, *args, **options):
        Category.objects.create(name="Electronics & Technology")
        Category.objects.create(name="Business Services")
        Category.objects.create(name="Vehicles & Transportation")
        Category.objects.create(name="Education & Training")
        Category.objects.create(name="Shopping & Fashion")
        amount = Category.objects.count()

        if amount == 5:
            self.stdout.write(self.style.SUCCESS("Create {a} categories".format(a=amount)))
        else:
            self.stderr.write(self.style.ERROR("Error"))
