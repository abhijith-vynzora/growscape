from django.db import models
from django.utils.text import slugify

# --- 1. SERVICE MODEL ---
class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    full_description = models.TextField(blank=True, help_text="Detailed explanation of the service.")
    features_list = models.TextField(
        help_text="Enter the bullet points from the brochure here, separated by commas or new lines."
    )
    cover_image = models.ImageField(upload_to='services/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# --- 2. PROJECT MODEL ---
class Project(models.Model):
    title = models.CharField(max_length=200)
    service_category = models.ForeignKey(
        Service, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='projects',
        help_text="Select which service category this project belongs to."
    )
    
    image = models.ImageField(upload_to='projects/')
    location = models.CharField(max_length=100, blank=True, help_text="e.g. Dubai Hills")
    description = models.TextField(blank=True, help_text="Description of work done.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)  
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Short introduction or quote.")
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="images"
    )
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title if self.title else f"Image {self.id}"

class Blog(models.Model):
    image = models.ImageField(upload_to="blogs/", help_text="Blog cover image")
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
class Testimonial(models.Model):
    name = models.CharField(
        max_length=100, help_text="Name of the person giving the testimonial"
    )
    image = models.ImageField(
        upload_to="testimonials/", blank=True, null=True, help_text="Profile picture"
    )
    review = models.TextField(help_text="Customer or client review")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image_fields = ["image"]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True) 
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"


class ServiceInquiry(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    service_type = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, related_name="inquiries"
    )

    # Status field removed

    preferred_date = models.DateField(blank=True, null=True, help_text="Preferred date for site visit")
    location = models.CharField(max_length=200, blank=True, help_text="Villa/Property Location")
    
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        service_name = self.service_type.name if self.service_type else "General"
        return f"{self.first_name} - {service_name}"