from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'builder'

# DRF router for API endpoints
router = DefaultRouter()
router.register(r'pages', views.PageViewSet, basename='api-page')
router.register(r'assets', views.AssetViewSet, basename='api-asset')
router.register(r'templates', views.TemplateViewSet, basename='api-template')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Frontend views
    path('', views.PageListView.as_view(), name='page_list'),
    path('builder/', views.PageBuilderView.as_view(), name='page_builder_new'),
    path('builder/<slug:slug>/', views.PageBuilderView.as_view(), name='page_builder_edit'),
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]
