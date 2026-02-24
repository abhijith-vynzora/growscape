from django import forms
from .models import Service, Project, TeamMember, Blog, Testimonial, Category, GalleryImage, ContactMessage, ServiceInquiry

# --- 1. SERVICE FORM ---
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'slug', 'full_description', 'features_list', 'cover_image']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Service Name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL Slug (auto-generated if empty)'}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed description...'}),
            'features_list': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Pruning, Planting, Design (separate by commas)'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

# --- 2. PROJECT FORM ---
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'service_category', 'image', 'location', 'description']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'service_category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dubai Hills'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

# --- 3. TEAM MEMBER FORM ---
class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'photo', 'bio']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short bio...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
    

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["image", "title", "description"]


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "image", "review"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["category", "title", "image"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "phone", "email", "message"]

class ServiceInquiryForm(forms.ModelForm):
    class Meta:
        model = ServiceInquiry
        # Removed 'status' from fields
        fields = ['first_name', 'last_name', 'phone', 'email', 'service_type', 'preferred_date', 'location', 'message']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }