from articles.utils import menu


def get_articles_context(request):
    return {'main_menu': menu,}
