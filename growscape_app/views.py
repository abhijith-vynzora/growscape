from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Lower
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import timedelta

# Import your models
from .models import Service, Project, TeamMember, Blog, Testimonial, Category, GalleryImage, ContactMessage, ServiceInquiry
# Import your forms
from .forms import ServiceForm, ProjectForm, TeamMemberForm, BlogForm, TestimonialForm, CategoryForm, GalleryImageForm, ContactForm, ServiceInquiryForm


import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from django.core.mail import EmailMultiAlternatives
# ==========================================
# 1. ADMIN AUTHENTICATION
# ==========================================

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, "authenticate/login.html") 

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("admin_dashboard") # Fixed redirect name based on urls.py
        else:
            messages.error(request, "Invalid credentials or unauthorized access.")

    return render(request, "authenticate/login.html")


@login_required(login_url="admin_login") 
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")


# ==========================================
# 2. DASHBOARD HOME
# ==========================================

@login_required(login_url="admin_login")
def admin_dashboard(request):
    now = timezone.now()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0)
    six_months_ago = now - timedelta(days=180)

    # Basic Counts
    total_projects = Project.objects.count()
    total_services = Service.objects.count()
    total_contacts = ContactMessage.objects.count()
    total_inquiries = ServiceInquiry.objects.count()
    projects_this_month = Project.objects.filter(created_at__gte=this_month_start).count()

    # Chart 1: Monthly Projects
    monthly_data = (
        Project.objects
        .filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    month_labels = [e['month'].strftime('%b %Y') for e in monthly_data]
    month_counts = [e['count'] for e in monthly_data]

    # Chart 2: Projects by Service
    by_service = (
        Project.objects
        .values('service_category__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:6]
    )
    service_labels = [e['service_category__name'] or 'Uncategorized' for e in by_service]
    service_counts = [e['count'] for e in by_service]

    # Recent Data Tables
    recent_projects = Project.objects.order_by('-created_at')[:6]
    recent_contacts = ContactMessage.objects.order_by('-created_at')[:5]
    recent_inquiries = ServiceInquiry.objects.select_related('service_type').order_by('-created_at')[:5]

    context = {
        'stats': {
            'total_projects': total_projects,
            'total_services': total_services,
            'total_contacts': total_contacts,
            'total_inquiries': total_inquiries,
            'projects_this_month': projects_this_month,
        },
        'month_labels': month_labels,
        'month_counts': month_counts,
        'service_labels': service_labels,
        'service_counts': service_counts,
        'recent_projects': recent_projects,
        'recent_contacts': recent_contacts,
        'recent_inquiries': recent_inquiries,
    }
    return render(request, "admin_pages/dashboard.html", context)


# ==========================================
# 3. SERVICE MANAGEMENT (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def service_list(request):
    services_qs = Service.objects.all().order_by("name")
    paginator = Paginator(services_qs, 10)
    page_number = request.GET.get("page")
    services = paginator.get_page(page_number)

    return render(request, "admin_pages/service_list.html", {"services": services})


@login_required(login_url="admin_login")
def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully!")
            return redirect("service_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ServiceForm()

    return render(request, "admin_pages/service_form.html", {"form": form})


@login_required(login_url="admin_login")
def service_update(request, pk):
    service_obj = get_object_or_404(Service, pk=pk)

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect("service_list")
    else:
        form = ServiceForm(instance=service_obj)

    return render(request, "admin_pages/service_form.html", {
        "form": form,
        "service": service_obj
    })


@login_required(login_url="admin_login")
def service_delete(request, pk):
    service_obj = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service_obj.delete()
        messages.success(request, "Service deleted successfully!")
    return redirect("service_list")


# ==========================================
# 4. PROJECT MANAGEMENT (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def project_list(request):
    projects_qs = Project.objects.all().order_by("-created_at")
    paginator = Paginator(projects_qs, 9)
    page_number = request.GET.get("page")
    projects = paginator.get_page(page_number)
    return render(request, "admin_pages/project_list.html", {
        "projects": projects,
        "all_services": Service.objects.all()
    })


@login_required(login_url="admin_login")
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully!")
            return redirect("project_list")
    else:
        form = ProjectForm()
    return render(request, "admin_pages/project_form.html", {
        "form": form,
        "all_services": Service.objects.all()
    })


@login_required(login_url="admin_login")
def project_update(request, pk):
    project_obj = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect("project_list")
    else:
        form = ProjectForm(instance=project_obj)
    return render(request, "admin_pages/project_form.html", {
        "form": form,
        "project": project_obj,
        "all_services": Service.objects.all()
    })


@login_required(login_url="admin_login")
def project_delete(request, pk):
    project_obj = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project_obj.delete()
        messages.success(request, "Project deleted successfully!")
    return redirect("project_list")


# ==========================================
# 5. TEAM MANAGEMENT (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def team_list(request):
    team_qs = TeamMember.objects.all().order_by("name")
    return render(request, "admin_pages/team_list.html", {"team_members": team_qs})


@login_required(login_url="admin_login")
def team_create(request):
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member added!")
            return redirect("team_list")
    else:
        form = TeamMemberForm()
    return render(request, "admin_pages/team_form.html", {"form": form})


@login_required(login_url="admin_login")
def team_update(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == "POST":
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member updated!")
            return redirect("team_list")
    else:
        form = TeamMemberForm(instance=member)
    return render(request, "admin_pages/team_form.html", {"form": form, "member": member})


@login_required(login_url="admin_login")
def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == "POST":
        member.delete()
        messages.success(request, "Team member removed.")
    return redirect("team_list")


# ==========================================
# 6. BLOGS (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def admin_blog_list(request):  # RENAMED from blog_list to fix URL error
    blogs_qs = Blog.objects.all().order_by("-created_at")
    paginator = Paginator(blogs_qs, 6)
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)

    return render(request, "admin_pages/blog_list.html", {"blogs": blogs})

@login_required(login_url="admin_login")
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post created!")
            return redirect("admin_blog_list")
    else:
        form = BlogForm()
    return render(request, "admin_pages/create_blog.html", {"form": form})

@login_required(login_url="admin_login")
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated!")
            return redirect("admin_blog_list")
    else:
        form = BlogForm(instance=blog)
    return render(request, "admin_pages/create_blog.html", {"form": form, "blog": blog})

@login_required(login_url="admin_login")
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted.")
    return redirect("admin_blog_list")


# ==========================================
# 7. GALLERY (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def gallery_images(request):
    categories = Category.objects.all().prefetch_related("images")
    category_pages = {}
    for category in categories:
        images_qs = category.images.all().order_by("-uploaded_at")
        paginator = Paginator(images_qs, 8)
        page_number = request.GET.get(f"page_{category.id}", 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        category_pages[category.id] = page_obj

    return render(
        request, "admin_pages/image_list.html",
        {"categories": categories, "category_pages": category_pages},
    )

@login_required(login_url="admin_login")
def add_image(request):
    categories = Category.objects.all()
    if request.method == "POST":
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        files = request.FILES.getlist("images")
        for file in files:
            GalleryImage.objects.create(
                category=category,
                title=file.name,
                image=file,
            )
        messages.success(request, "Images uploaded successfully!")
        return redirect("list_image")
        
    return render(request, "admin_pages/add_image.html", {"categories": categories})

@login_required(login_url="admin_login")
def delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    if request.method == "POST":
        image.delete()
        messages.success(request, "Image deleted successfully!")
        return redirect("list_image")
    return render(request, "admin_pages/image_list.html", {"image": image})


@login_required(login_url="admin_login")
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)
    return render(request, "admin_pages/category_list.html", {"categories": categories})


@login_required(login_url="admin_login")
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Category created successfully!") 
            return redirect("category_list")
    return render(request, "admin_pages/add_category.html")


@login_required(login_url="admin_login")
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect("category_list")
    return redirect("category_list") 


@login_required(login_url="admin_login")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!") 
        return redirect("category_list")
    return redirect("category_list")


# ==========================================
# 8. TESTIMONIALS (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def testimonial_list(request):
    testimonials_list = Testimonial.objects.all().order_by(Lower("name"))
    paginator = Paginator(testimonials_list, 6)
    page_number = request.GET.get("page")
    testimonials = paginator.get_page(page_number)
    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})


@login_required(login_url="admin_login")
def testimonial_create(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully!")
            return redirect("review_list")
    else:
        form = TestimonialForm()
    return render(request, "admin_pages/create_review.html", {"form": form})


@login_required(login_url="admin_login")
def testimonial_update(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully!")
            return redirect("review_list")
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, "admin_pages/review_list.html", {"form": form, "testimonial": testimonial})


@login_required(login_url="admin_login")
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully!")
        return redirect("review_list")
    return render(request, "admin_pages/review_list.html", {"testimonial": testimonial})


# ==========================================
# 9. CONTACTS & INQUIRIES (ADMIN)
# ==========================================

@login_required(login_url="admin_login")
def view_contacts(request):
    contacts = ContactMessage.objects.all().order_by("-created_at")
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "admin_pages/view_contacts.html", {"contacts": page_obj})

@login_required(login_url="admin_login")
def delete_contact(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        contact.delete()
    return redirect("view_contacts")

@login_required(login_url="admin_login")
def inquiry_list(request):
    inquiries_qs = ServiceInquiry.objects.all().order_by("-created_at")
    paginator = Paginator(inquiries_qs, 10)
    page_number = request.GET.get("page")
    inquiries = paginator.get_page(page_number)
    return render(request, "admin_pages/inquiry_list.html", {"inquiries": inquiries})

@login_required(login_url="admin_login")
def inquiry_delete(request, pk):
    inquiry = get_object_or_404(ServiceInquiry, pk=pk)
    if request.method == "POST":
        inquiry.delete()
        messages.success(request, "Inquiry deleted successfully!")
    return redirect("inquiry_list")


# ==========================================
# 10. FRONTEND VIEWS (PUBLIC WEBSITE)
# ==========================================

def home(request):
    context = {
        'services': Service.objects.all(),
        'projects': Project.objects.all()[:6],
        'testimonials': Testimonial.objects.all()[:5],
        'blogs': Blog.objects.all()[:3],
        'categories': Service.objects.all()
    }
    return render(request, 'frontend/index.html', context)

def about(request):
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request, "frontend/about.html", {"team_members": team_members, "testimonials": testimonials})

def services_page(request):
    services = Service.objects.all()
    return render(request, "frontend/service.html", {"services": services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    all_services = Service.objects.all()

    # Handle both comma-separated and newline-separated features
    raw = service.features_list or ''
    if ',' in raw:
        features = [f.strip() for f in raw.split(',') if f.strip()]
    else:
        features = [f.strip() for f in raw.splitlines() if f.strip()]

    return render(request, "frontend/service-single.html", {
        "service": service,
        "all_services": all_services,
        "features": features,
    })

def portfolio(request):
    projects = Project.objects.select_related('service_category').all()
    categories = Service.objects.filter(projects__isnull=False).distinct()
    return render(request, "frontend/project.html", {
        "projects": projects,
        "categories": categories,
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "frontend/project-single.html", {
        "project": project,
    })

def team_page(request):
    team_members = TeamMember.objects.all()
    return render(request, "frontend/team.html", {"team_members": team_members})

def public_blog_list(request):
    blogs = Blog.objects.all().order_by("-created_at")
    paginator = Paginator(blogs, 9)
    page = request.GET.get('page')
    blogs_paged = paginator.get_page(page)
    return render(request, "frontend/blog.html", {"blogs": blogs_paged})

def blog_list(request):
    all_blogs = Blog.objects.all()
    paginator = Paginator(all_blogs, 6)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, "frontend/blog.html", {"blogs": blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    recent_blogs = Blog.objects.exclude(slug=slug).order_by('-created_at')[:3]
    return render(request, "frontend/blog-single.html", {
        "blog": blog,
        "recent_blogs": recent_blogs,
    })

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('msg', '').strip()

        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message,
        )
        messages.success(request, "Your message has been sent successfully! We'll get back to you soon.")
        return redirect('contact')

    return render(request, "frontend/contact.html")

# def service_inquiry(request):
#     services = Service.objects.all()
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name', '').strip()
#         last_name = request.POST.get('last_name', '').strip()
#         email = request.POST.get('email', '').strip()
#         phone = request.POST.get('phone', '').strip()
#         service_id = request.POST.get('service_type')
#         preferred_date = request.POST.get('preferred_date') or None
#         location = request.POST.get('location', '').strip()
#         message = request.POST.get('message', '').strip()

#         ServiceInquiry.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             phone=phone,
#             service_type_id=service_id or None,
#             preferred_date=preferred_date,
#             location=location,
#             message=message,
#         )
#         messages.success(request, "Your inquiry has been submitted! We'll contact you shortly.")
#         return redirect('service_inquiry')

#     return render(request, "frontend/service-inquiry.html", {"services": services})


from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

def service_inquiry(request):
    services = Service.objects.all()
    if request.method == 'POST':
        # 1. Capture Form Data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email_address = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        service_id = request.POST.get('service_type')
        location = request.POST.get('location', '').strip()
        message = request.POST.get('message', '').strip()

        # 2. Save to Database
        inquiry = ServiceInquiry.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email_address,
            phone=phone,
            service_type_id=service_id or None,
            location=location,
            message=message,
        )

        # 3. Email Logic using your exact requested style
        service_title = inquiry.service_type.name if inquiry.service_type else "General Service"
        subject = "New Service Inquiry"

        html_message = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0; padding:0; background-color:#f4f4f4; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="background:#2D4636; padding:30px; text-align:center;">
                            <h2 style="margin:0; color:#ffffff;">New Service Inquiry</h2>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:30px;">
                            <p style="color:#555; font-size:15px;">A new inquiry has been submitted through the Growscape website.</p>
                            <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e0e0e0; border-radius:6px;">
                                <tr>
                                    <td style="padding:12px; font-weight:bold;">Full Name</td>
                                    <td style="padding:12px;">{first_name} {last_name}</td>
                                </tr>
                                <tr style="background:#f8f9fa;">
                                    <td style="padding:12px; font-weight:bold;">Email</td>
                                    <td style="padding:12px;">{email_address}</td>
                                </tr>
                                <tr>
                                    <td style="padding:12px; font-weight:bold;">Mobile</td>
                                    <td style="padding:12px;">{phone}</td>
                                </tr>
                                <tr style="background:#f8f9fa;">
                                    <td style="padding:12px; font-weight:bold;">Service</td>
                                    <td style="padding:12px;">{service_title}</td>
                                </tr>
                                <tr>
                                    <td style="padding:12px; font-weight:bold;">Location</td>
                                    <td style="padding:12px;">{location}</td>
                                </tr>
                            </table>
                            <p style="margin-top:20px;"><b>Message:</b> {message}</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background:#f8f9fa; padding:20px; text-align:center;">
                            <p style="margin:0; font-size:13px; color:#888;">Growscape Landscaping LLC</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            settings.EMAIL_HOST_USER,
            ['theofaber26@gmail.com'],
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)

        messages.success(request, "Your inquiry has been submitted!")
        return redirect('service_inquiry')

    return render(request, "frontend/service-inquiry.html", {"services": services})

def gallery(request):
    categories = Category.objects.all()
    gallery_images = GalleryImage.objects.all()

    return render(request, "frontend/gallery.html", {
        "categories": categories,
        "gallery_images": gallery_images,
    })