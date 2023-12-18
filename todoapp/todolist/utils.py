
from .models import *



menu = []


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        imp = Importance.objects.all()
        context['menu'] = menu
        context['sygnif'] = imp

        return context



