from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemplateViewSet, TemplateRenderLogViewSet

router = DefaultRouter()
router.register(r"templates", TemplateViewSet, basename="template")
router.register(r"render-logs", TemplateRenderLogViewSet,
                basename="render-log")

urlpatterns = [
    path("", include(router.urls)),
]
