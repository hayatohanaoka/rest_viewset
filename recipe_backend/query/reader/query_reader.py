from pathlib import Path
from django.conf import settings

class Reader:
    @classmethod
    def get_by_file(cls, file):
        path = Path.joinpath(settings.BASE_DIR, 'query', 'sql', file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        f.close()
        return content
