from shop.models import Category


def category_list(request):
    data = {'category_list': Category.objects.all()}
    return data
