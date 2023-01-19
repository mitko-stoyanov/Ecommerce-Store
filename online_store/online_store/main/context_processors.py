from online_store.store.models import Category, WishList


def show_categories(request):
    all_categories = Category.objects.all()
    try:
        wish_list = WishList.objects.filter(owner=request.user)
    except:
        wish_list = None
    result = {
        'categories': all_categories,
        'wish_list': wish_list,
    }

    return result
