import logging

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import NotificationTemplate, TemplateRenderLog
from .serializers import (
    NotificationTemplateSerializer,
    TemplateCreateSerializer,
    TemplateRenderLogSerializer,
    TemplateRenderResponseSerializer,
    TemplateRenderSerializer,
)
from .services import TemplateService, TemplateVersionService

logger = logging.getLogger(__name__)


class TemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for managing notification templates."""

    queryset = NotificationTemplate.objects.filter(is_active=True).select_related(
        "content"
    )
    serializer_class = NotificationTemplateSerializer

    @swagger_auto_schema(
        method="post",
        request_body=TemplateCreateSerializer,
        responses={201: NotificationTemplateSerializer},
    )
    @action(detail=False, methods=["post"])
    def create_template(self, request):
        """Create a new template or new version if template exists."""
        serializer = TemplateCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        existing_template = TemplateService.get_template(
            data["name"], data["language"], data["template_type"], use_cache=False
        )

        if existing_template:
            # Create new version
            new_version = TemplateVersionService.create_new_version(
                data["name"],
                data["language"],
                data["template_type"],
                data.get("subject", ""),
                data["body"],
                data.get("description"),
            )
            response_serializer = NotificationTemplateSerializer(new_version)
            logger.info(
                f"Created new version for template: {data['name']} ({data['language']}, {data['template_type']})"
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Create new template
            template = NotificationTemplate.objects.create(
                name=data["name"],
                language=data["language"],
                template_type=data["template_type"],
                description=data.get("description"),
            )

            from .models import TemplateContent

            TemplateContent.objects.create(
                template=template, subject=data.get("subject", ""), body=data["body"]
            )

            response_serializer = NotificationTemplateSerializer(template)
            logger.info(
                f"Created new template: {data['name']} ({data['language']}, {data['template_type']})"
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method="post",
        request_body=TemplateRenderSerializer,
        responses={200: TemplateRenderResponseSerializer},
    )
    @action(detail=False, methods=["post"])
    def render(self, request):
        """Render a template with provided context."""
        serializer = TemplateRenderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            rendered = TemplateService.render_template(
                name=data["template_name"],
                context=data["context"],
                language=data["language"],
                template_type=data["template_type"],
                requested_by=data.get("requested_by"),
            )

            response_serializer = TemplateRenderResponseSerializer(rendered)
            logger.info(
                f"Successfully rendered template: {data['template_name']} ({data['language']}, {data['template_type']})"
            )
            return Response(response_serializer.data)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        method="get",
        responses={
            200: openapi.Response(
                "List of available variables", type=openapi.TYPE_ARRAY
            )
        },
    )
    @action(detail=True, methods=["get"])
    def variables(self, request, pk=None):
        """Get available variables for a template."""
        template = self.get_object()
        variables = TemplateService.get_available_variables(
            template.name, template.language, template.template_type
        )
        return Response({"variables": variables})

    @swagger_auto_schema(method="post", responses={200: NotificationTemplateSerializer})
    @action(detail=True, methods=["post"])
    def rollback(self, request, pk=None):
        """Rollback to a previous version."""
        template = self.get_object()
        version = request.data.get("version")

        if not version:
            return Response(
                {"error": "Version number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            rolled_back = TemplateVersionService.rollback_to_version(
                template.name, template.language, template.template_type, version
            )
            serializer = NotificationTemplateSerializer(rolled_back)
            return Response(serializer.data)

        except NotificationTemplate.DoesNotExist:
            return Response(
                {"error": f"Version {version} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "template_name": openapi.Schema(type=openapi.TYPE_STRING),
                "language": openapi.Schema(type=openapi.TYPE_STRING, default="en"),
                "template_type": openapi.Schema(
                    type=openapi.TYPE_STRING, default="email"
                ),
                "context": openapi.Schema(type=openapi.TYPE_OBJECT),
                "requested_by": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            202: openapi.Response(
                "Task accepted",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "task_id": openapi.Schema(type=openapi.TYPE_STRING),
                        "status": openapi.Schema(type=openapi.TYPE_STRING),
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )
    @action(detail=False, methods=["post"], url_path="render-async")
    def render_async(self, request):
        """Render template asynchronously using Celery."""
        from .services import CeleryService

        template_name = request.data.get("template_name")
        context = request.data.get("context", {})
        language = request.data.get("language", "en")
        template_type = request.data.get("template_type", "email")
        requested_by = request.data.get("requested_by")

        if not template_name:
            return Response(
                {"error": "template_name is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            task_id = CeleryService.trigger_async_render(
                template_name, context, language, template_type, requested_by
            )

            return Response(
                {
                    "task_id": task_id,
                    "status": "accepted",
                    "message": f"Template rendering started for {template_name}",
                    "monitor_url": f"/api/v1/tasks/{task_id}/status/",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            logger.error(f"Error triggering async render: {str(e)}")
            return Response(
                {"error": "Failed to start async rendering"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "render_requests": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_OBJECT),
                )
            },
        ),
        responses={202: openapi.Response("Bulk task accepted")},
    )
    @action(detail=False, methods=["post"], url_path="bulk-render")
    def bulk_render(self, request):
        """Bulk render multiple templates asynchronously."""
        from .services import CeleryService

        render_requests = request.data.get("render_requests", [])

        if not render_requests:
            return Response(
                {"error": "render_requests is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            task_id = CeleryService.trigger_bulk_render(render_requests)

            return Response(
                {
                    "task_id": task_id,
                    "status": "accepted",
                    "message": f"Bulk rendering started for {len(render_requests)} templates",
                    "monitor_url": f"/api/v1/tasks/{task_id}/status/",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            logger.error(f"Error triggering bulk render: {str(e)}")
            return Response(
                {"error": "Failed to start bulk rendering"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        method="post", responses={202: openapi.Response("Cache warmup started")}
    )
    @action(detail=False, methods=["post"], url_path="warm-cache")
    def warm_cache(self, request):
        """Trigger cache warmup task."""
        from .services import CeleryService

        try:
            task_id = CeleryService.trigger_cache_warmup()

            return Response(
                {
                    "task_id": task_id,
                    "status": "accepted",
                    "message": "Cache warmup started",
                },
                status=status.HTTP_202_ACCEPTED,
            )

        except Exception as e:
            logger.error(f"Error triggering cache warmup: {str(e)}")
            return Response(
                {"error": "Failed to start cache warmup"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TemplateRenderLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing template render logs."""

    queryset = TemplateRenderLog.objects.select_related("template")
    serializer_class = TemplateRenderLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        template_id = self.request.query_params.get("template_id")
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        return queryset
