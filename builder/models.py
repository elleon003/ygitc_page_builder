from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Page(models.Model):
    """
    Model representing a page created with the page builder
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.JSONField(default=dict, blank=True, help_text="GrapesJS JSON content")
    html = models.TextField(blank=True, help_text="Generated HTML content")
    css = models.TextField(blank=True, help_text="Generated CSS content")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pages'
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('builder:page_detail', kwargs={'slug': self.slug})


class Asset(models.Model):
    """
    Model for storing assets used in page builder (images, etc.)
    """
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='assets/')
    file_type = models.CharField(max_length=50, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Template(models.Model):
    """
    Model for storing reusable page templates
    """
    name = models.CharField(max_length=200)
    content = models.JSONField(default=dict, help_text="GrapesJS JSON content")
    thumbnail = models.ImageField(upload_to='templates/', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='templates'
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
