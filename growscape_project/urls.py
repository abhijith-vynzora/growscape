from django.contrib import admin
from django.urls import path, include  
from django.conf import settings        
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.contrib.sitemaps.views import sitemap
from growscape_app.sitemap import StaticViewSitemap, BlogSitemap, ServiceSitemap, ProjectSitemap
from django.http import HttpResponse
import os

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'service': ServiceSitemap,
    'project': ProjectSitemap,
}

def robots_txt(request):
    file_path = os.path.join(settings.BASE_DIR, 'growscape_project', 'robots.txt')
    with open(file_path, 'r') as f:
        return HttpResponse(f.read(), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('growscape_app.urls')),
    
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'growscape_app.views.custom_404'