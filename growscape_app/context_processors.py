from .models import Service, Blog

def nav_data(request):
    return {
        'nav_services': Service.objects.all(),
        'nav_blogs': Blog.objects.all()[:4],
    }