from django.db.models import Model
from django.urls import reverse


class TestUtils:
    model_class: type[Model]
    base_url_name: str

    def get_count(self, **filters) -> int:
        return self.model_class.objects.filter(**filters).count()

    def retrieve(self, id=None, **filter) -> Model:
        if id:
            filter['id'] = id
        return self.model_class.objects.get(**filter)

    def filter(self, **filters):
        return self.model_class.objects.filter(**filters)

    def detail_url(self, *args, **kwargs) -> str:
        return reverse(f'{self.base_url_name}-detail', args=args, kwargs=kwargs)

    def list_url(self, *args, **kwargs) -> str:
        return reverse(f'{self.base_url_name}-list', args=args, kwargs=kwargs)
