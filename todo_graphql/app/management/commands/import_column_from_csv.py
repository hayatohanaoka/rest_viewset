import csv
from django.core.management import BaseCommand
from django.conf import settings
import os

from ...models import Column

class Command(BaseCommand):
    help = 'columns.csv を読み込んで挿入'

    def handle(self, *args, **kwargs):
        csv_file = os.path.join(settings.BASE_DIR, 'resources', 'columns.csv')
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Column.objects.create(
                    title=row['title'],
                    description=row['description'],
                    user_id=row['user_id']
                )
            f.close()
        print('インポート完了')
