from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Page, Asset, Template
from .serializers import PageSerializer, AssetSerializer, TemplateSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.created_by == request.user


class PageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing pages
    """
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        """
        This view should return a list of all pages
        for the currently authenticated user.
        """
        user = self.request.user
        # Staff can see all pages, otherwise users only see their own
        if user.is_staff:
            return Page.objects.all()
        return Page.objects.filter(created_by=user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        """
        Publish or unpublish a page
        """
        page = self.get_object()
        page.is_published = not page.is_published
        page.save()
        return Response({'status': 'page status updated', 
                         'is_published': page.is_published})


class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing assets
    """
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Asset.objects.all()
        return Asset.objects.filter(created_by=user)


class TemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing templates
    """
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Template.objects.all()
        # Users can see their own templates and public templates
        return Template.objects.filter(created_by=user) | Template.objects.filter(is_public=True)


# Frontend Views
class PageBuilderView(TemplateView):
    """
    Main page builder view
    """
    template_name = 'builder/page_builder.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_slug = kwargs.get('slug')
        if page_slug:
            context['page'] = get_object_or_404(Page, slug=page_slug, created_by=self.request.user)
        return context


class PageListView(ListView):
    """
    List view for pages
    """
    model = Page
    template_name = 'builder/page_list.html'
    context_object_name = 'pages'
    
    def get_queryset(self):
        return Page.objects.filter(created_by=self.request.user)


class PageDetailView(DetailView):
    """
    Detail view for showing published pages
    """
    model = Page
    template_name = 'builder/page_detail.html'
    context_object_name = 'page'
    
    def get(self, request, *args, **kwargs):
        """
        Return the actual rendered HTML of the page for public viewing
        """
        page = self.get_object()
        if not page.is_published and page.created_by != request.user:
            return HttpResponse("This page is not published", status=403)
        
        if 'raw' in request.GET:
            # Return just the HTML content
            response = HttpResponse(page.html)
            response['Content-Type'] = 'text/html'
            return response
        
        return super().get(request, *args, **kwargs)
