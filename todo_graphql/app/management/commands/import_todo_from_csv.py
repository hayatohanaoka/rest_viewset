import csv
from django.core.management import BaseCommand
from django.conf import settings
import os

from ...models import ToDo

class Command(BaseCommand):
    help = 'todo.csv を読み込んで挿入'

    def handle(self, *args, **kwargs):
        csv_file = os.path.join(settings.BASE_DIR, 'resources', 'todo.csv')
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ToDo.objects.create(
                    title=row['title'],
                    description=row['description'],
                    priority=int(row['priority']),
                    deadline=row['deadline'],
                    is_completed=row['is_completed'],
                    user_id=row['user_id']
                )
            f.close()
        print('インポート完了')
