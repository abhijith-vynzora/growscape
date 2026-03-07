from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog, Service, Project


class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return [
            "home", "about", "services", "portfolio", "gallery",
            "contact", "service_inquiry", "public_blog_list", "public_team"
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Blog.objects.all()

    def location(self, obj):
        return reverse('blog_detail', kwargs={'slug': obj.slug})


class ServiceSitemap(Sitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return reverse('service_detail', kwargs={'slug': obj.slug})


class ProjectSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Project.objects.all()

    def location(self, obj):
        return reverse('project_detail', kwargs={'pk': obj.pk})