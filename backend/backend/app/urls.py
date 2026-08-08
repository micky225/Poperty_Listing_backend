from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AgentViewSet,
    BlogPostViewSet,
    PropertyViewSet,
    TestimonialViewSet,
    comparable_properties,
    meta_view,
)

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'blog-posts', BlogPostViewSet, basename='blog-post')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('meta/', meta_view, name='meta'),
    path('properties/<int:pk>/comparables/', comparable_properties, name='property-comparables'),
    path('', include(router.urls)),
]
