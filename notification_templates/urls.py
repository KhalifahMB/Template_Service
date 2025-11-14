from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TemplateRenderLogViewSet, TemplateViewSet

router = DefaultRouter()
router.register(r"templates", TemplateViewSet, basename="template")
router.register(r"render-logs", TemplateRenderLogViewSet, basename="render-log")

urlpatterns = [
    path("", include(router.urls)),
]
