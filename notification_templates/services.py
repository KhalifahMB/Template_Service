import logging

from django.conf import settings
from django.core.cache import cache

from .models import NotificationTemplate, TemplateRenderLog
from .utils import TemplateRenderer

logger = logging.getLogger(__name__)


class TemplateService:
    """Service layer for template operations."""

    @staticmethod
    def get_template(name, language="en", template_type="email", use_cache=True):
        """Get template with caching support."""
        cache_key = f"template_{name}_{language}_{template_type}"

        if use_cache:
            cached_template = cache.get(cache_key)
            if cached_template:
                logger.debug(f"Cache hit for template: {cache_key}")
                logger.info(
                    f"Retrieved template {name} ({language}, {template_type}) from cache"
                )
                return cached_template

        template = NotificationTemplate.get_active_template(
            name, language, template_type
        )

        if template and use_cache:
            cache.set(cache_key, template, settings.CACHE_TTL)
            logger.debug(f"Cached template: {cache_key}")
            logger.info(
                f"Cached template {name} ({language}, {template_type}) with TTL {settings.CACHE_TTL}"
            )

        return template

    @staticmethod
    def clear_template_cache(name, language="en", template_type="email"):
        """Clear cache for a specific template."""
        cache_key = f"template_{name}_{language}_{template_type}"
        cache.delete(cache_key)
        logger.info(f"Cleared cache for template {name} ({language}, {template_type})")

    @staticmethod
    def render_template(
        name, context, language="en", template_type="email", requested_by=None
    ):
        """Render template with variables substitution."""
        try:
            template = TemplateService.get_template(name, language, template_type)

            if not template:
                raise ValueError(f"Template not found: {name} ({language})")

            renderer = TemplateRenderer(template)
            result = renderer.render(context)

            # Log the rendering
            TemplateRenderLog.objects.create(
                template=template,
                context_used=context,
                rendered_subject=result.get("subject"),
                rendered_body=result.get("body"),
                success=True,
                requested_by=requested_by,
            )

            logger.info(f"Successfully rendered template: {name} for {requested_by}")
            return result

        except Exception as e:
            # Log failed rendering
            template = NotificationTemplate.get_active_template(
                name, language, template_type
            )
            if template:
                TemplateRenderLog.objects.create(
                    template=template,
                    context_used=context,
                    rendered_body="",
                    success=False,
                    error_message=str(e),
                    requested_by=requested_by,
                )

            logger.error(f"Failed to render template {name}: {str(e)}")
            raise

    @staticmethod
    def get_available_variables(name, language="en", template_type="email"):
        """Get available variables for a template."""
        template = TemplateService.get_template(name, language, template_type)
        if template and hasattr(template, "content"):
            return template.content.extracted_variables
        return []

    @staticmethod
    def get_templates_by_type(template_type="email"):
        """Get all active templates of a specific type."""
        return NotificationTemplate.objects.filter(
            template_type=template_type, is_active=True
        ).select_related("content")


class TemplateVersionService:
    """Service for template version management."""

    @staticmethod
    def create_new_version(
        template_name, language, template_type, subject, body, description=None
    ):
        """Create a new version of a template."""
        current_template = NotificationTemplate.get_active_template(
            template_name, language, template_type
        )

        if not current_template:
            raise ValueError(f"Template not found: {template_name}")

        new_version = current_template.create_new_version(subject, body, description)
        return new_version

    @staticmethod
    def rollback_to_version(template_name, language, template_type, version):
        """Rollback to a specific version."""
        target_template = NotificationTemplate.objects.get(
            name=template_name,
            language=language,
            template_type=template_type,
            version=version,
        )

        # Deactivate all versions
        NotificationTemplate.objects.filter(
            name=template_name, language=language, template_type=template_type
        ).update(is_active=False)

        # Activate target version
        target_template.is_active = True
        target_template.save()

        # Clear cache
        TemplateService.clear_template_cache(template_name, language, template_type)

        logger.info(f"Rolled back {template_name} to version {version}")
        return target_template


class CeleryService:
    """Service for triggering Celery tasks."""

    @staticmethod
    def trigger_async_render(
        template_name, context, language="en", template_type="email", requested_by=None
    ):
        """Trigger asynchronous template rendering."""
        from .tasks import render_template_async

        task = render_template_async.delay(
            template_name=template_name,
            context=context,
            language=language,
            template_type=template_type,
            requested_by=requested_by,
        )

        logger.info(
            f"Triggered async render task {task.id} for template {template_name}"
        )
        return task.id

    @staticmethod
    def trigger_bulk_render(render_requests):
        """Trigger bulk template rendering."""
        from .tasks import bulk_render_templates

        task = bulk_render_templates.delay(render_requests)

        logger.info(
            f"Triggered bulk render task {task.id} for {len(render_requests)} templates"
        )
        return task.id

    @staticmethod
    def trigger_cache_warmup():
        """Trigger cache warmup task."""
        from .tasks import warm_template_cache

        task = warm_template_cache.delay()

        logger.info(f"Triggered cache warmup task {task.id}")
        return task.id

    @staticmethod
    def trigger_template_cache_update(template_id):
        """Trigger cache update for specific template."""
        from .tasks import update_template_cache_for_template

        task = update_template_cache_for_template.delay(template_id)

        logger.info(f"Triggered cache update task {task.id} for template {template_id}")
        return task.id
