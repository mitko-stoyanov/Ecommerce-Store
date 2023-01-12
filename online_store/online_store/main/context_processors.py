from online_store.store.models import Category


def show_categories(request):
    all_categories = Category.objects.all()
    result = {
        'categories': all_categories,
    }

    return result