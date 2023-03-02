from django.shortcuts import redirect
from django.views.generic import TemplateView

from .models import Slider, IndexCats, Parser
from .tasks import parse_all_task
from shop.models import Product


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['sliders'] = Slider.objects.all()
        context['page_cats'] = IndexCats.objects.get(name='Категории')
        context['random_products'] = Product.objects.all().order_by('?')[:8]
        return context


class FillDataAdminView(TemplateView):
    template_name = "admin/fill_database.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            _all = list(Parser.objects.filter(is_active=True).values())
            parse_all_task.delay(_all)
            return super().get(request, *args, **kwargs)
        else:
            return redirect('index')
