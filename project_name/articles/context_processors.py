from articles.views import check_bookmark

def context_processor(request):
    context = (check_bookmark(request))
    return context
