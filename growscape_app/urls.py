from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    # ==============================Authentication URLs=========================
    path("admin-login/", views.admin_login, name="admin_login"),
    path("admin-logout/", views.admin_logout, name="admin_logout"),

    # ==============================Dashboard=========================
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # ==============================Services=========================
    path("dashboard/services/", views.service_list, name="service_list"),
    path("dashboard/services/add/", views.service_create, name="service_create"),
    path("dashboard/services/update/<int:pk>/", views.service_update, name="service_update"),
    path("dashboard/services/delete/<int:pk>/", views.service_delete, name="service_delete"),

    # ==============================Projects=========================
    path("dashboard/projects/", views.project_list, name="project_list"),
    path("dashboard/projects/add/", views.project_create, name="project_create"),
    path("dashboard/projects/update/<int:pk>/", views.project_update, name="project_update"),
    path("dashboard/projects/delete/<int:pk>/", views.project_delete, name="project_delete"),

    # ==============================Team (Admin)=========================
    path("dashboard/team/", views.team_list, name="team_list"),
    path("dashboard/team/add/", views.team_create, name="team_create"),
    path("dashboard/team/update/<int:pk>/", views.team_update, name="team_update"),
    path("dashboard/team/delete/<int:pk>/", views.team_delete, name="team_delete"),

    # ==============================Contacts (Admin)=========================
    path("dashboard/contacts/", views.view_contacts, name="view_contacts"),
    path("dashboard/contacts/delete/<int:pk>/", views.delete_contact, name="delete_contact"),

    # ==============================Blogs (Admin) =========================
    # RENAMED VIEW FUNCTION TO 'admin_blog_list' TO AVOID CONFLICT
    path("dashboard/blogs/", views.admin_blog_list, name="admin_blog_list"),       
    path("dashboard/blogs/add/", views.blog_create, name="blog_create"),
    path("dashboard/blogs/update/<int:pk>/", views.blog_update, name="blog_update"),
    path("dashboard/blogs/delete/<int:pk>/", views.blog_delete, name="blog_delete"),

    # ==============================Gallery=========================
    path("dashboard/gallery/", views.gallery_images, name="list_image"),
    path("dashboard/gallery/categories/", views.category_list, name="category_list"),
    path("dashboard/gallery/categories/add/", views.add_category, name="add_category"),
    path("dashboard/gallery/categories/update/<int:pk>/", views.update_category, name="update_category"),
    path("dashboard/gallery/categories/delete/<int:pk>/", views.delete_category, name="delete_category"),
    path("dashboard/gallery/add/", views.add_image, name="add_image"),
    path("dashboard/gallery/delete/<int:image_id>/", views.delete_image, name="delete_image"),

    # ==============================Testimonials=========================
    path("dashboard/testimonials/", views.testimonial_list, name="review_list"),
    path("dashboard/testimonials/add/", views.testimonial_create, name="testimonial_create"),
    path("dashboard/testimonials/<int:pk>/edit/", views.testimonial_update, name="testimonial_update"),
    path("dashboard/testimonials/<int:pk>/delete/", views.testimonial_delete, name="testimonial_delete"),

    # ==============================Inquiries=========================
    path("dashboard/inquiries/", views.inquiry_list, name="inquiry_list"),
    path("dashboard/inquiries/delete/<int:pk>/", views.inquiry_delete, name="inquiry_delete"),

    # ==============================Frontend URLs=========================
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services_page, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('inquiry/', views.service_inquiry, name='service_inquiry'),
    path('projects/', views.portfolio, name='portfolio'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('blogs/', views.public_blog_list, name='public_blog_list'), 
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('team/', views.team_page, name='public_team'), 
    path('contact/', views.contact, name='contact'),
    path("gallery/", views.gallery, name="gallery"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)