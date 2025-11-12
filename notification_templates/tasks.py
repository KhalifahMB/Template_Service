from celery import shared_task
import logging
from django.core.cache import cache
from django.db import transaction
from .models import NotificationTemplate, TemplateRenderLog
from .services import TemplateService

logger = logging.getLogger(__name__)


@shared_task
def warm_template_cache():
    """Warm up cache for frequently used templates."""
    try:
        frequent_templates = NotificationTemplate.objects.filter(
            is_active=True
        ).select_related('content')[:50]  # Cache top 50 templates

        cache_keys = []
        for template in frequent_templates:
            cache_key = f"template_{template.name}_{template.language}_{template.template_type}"
            cache.set(cache_key, template, 1800)  # 30 minutes
            cache_keys.append(cache_key)

        logger.info(f"Warmed up cache for {len(frequent_templates)} templates")
        return {
            'status': 'success',
            'templates_cached': len(frequent_templates),
            'cache_keys': cache_keys
        }

    except Exception as e:
        logger.error(f"Error warming template cache: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task
def cleanup_old_render_logs(days=30):
    """Clean up old render logs."""
    from django.utils import timezone
    from datetime import timedelta

    try:
        cutoff_date = timezone.now() - timedelta(days=days)

        with transaction.atomic():
            # Get count before deletion for logging
            logs_to_delete = TemplateRenderLog.objects.filter(
                created_at__lt=cutoff_date
            )
            count_before = logs_to_delete.count()

            # Delete in chunks to avoid large transactions
            deleted_count = 0
            batch_size = 1000

            while True:
                batch = logs_to_delete[:batch_size]
                if not batch:
                    break

                batch_ids = list(batch.values_list('id', flat=True))
                deleted, _ = TemplateRenderLog.objects.filter(
                    id__in=batch_ids).delete()
                deleted_count += deleted

                logger.info(f"Deleted batch of {deleted} render logs")

        logger.info(
            f"Cleaned up {deleted_count} old render logs (older than {days} days)")
        return {
            'status': 'success',
            'logs_deleted': deleted_count,
            'days_retained': days
        }

    except Exception as e:
        logger.error(f"Error cleaning up render logs: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task
def health_check():
    """Celery health check task."""
    try:
        # Check database connection
        template_count = NotificationTemplate.objects.filter(
            is_active=True).count()

        # Check cache connection
        cache.set('health_check', 'ok', 60)
        cache_status = cache.get('health_check') == 'ok'

        logger.info(
            f"Health check: DB={template_count} templates, Cache={'OK' if cache_status else 'FAILED'}")

        return {
            'status': 'healthy',
            'database': 'connected',
            'cache': 'connected' if cache_status else 'disconnected',
            'active_templates': template_count,
            'timestamp': timezone.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            'status': 'unhealthy',
            'error': str(e)
        }


@shared_task
def render_template_async(template_name, context, language='en', template_type='email', requested_by=None):
    """Render template asynchronously."""
    try:
        from .services import TemplateService

        result = TemplateService.render_template(
            template_name, context, language, template_type, requested_by
        )

        logger.info(f"Async template rendering completed for {template_name}")
        return {
            'status': 'success',
            'template_name': template_name,
            'rendered_subject': result.get('subject'),
            'rendered_body_length': len(result.get('body', '')),
            'requested_by': requested_by
        }

    except Exception as e:
        logger.error(
            f"Async template rendering failed for {template_name}: {str(e)}")
        return {
            'status': 'error',
            'template_name': template_name,
            'error': str(e)
        }


@shared_task
def bulk_render_templates(render_requests):
    """
    Bulk render multiple templates asynchronously.

    Args:
        render_requests: List of dictionaries with template rendering parameters
        Example:
        [
            {
                'template_name': 'welcome_email',
                'context': {'user_name': 'John', 'company_name': 'Test Co'},
                'language': 'en'
            },
            {
                'template_name': 'password_reset', 
                'context': {'user_name': 'Jane', 'reset_link': '...'},
                'language': 'en'
            }
        ]
    """
    try:
        from .services import TemplateService

        results = []
        for request in render_requests:
            try:
                result = TemplateService.render_template(
                    template_name=request['template_name'],
                    context=request['context'],
                    language=request.get('language', 'en'),
                    template_type=request.get('template_type', 'email'),
                    requested_by=request.get('requested_by', 'bulk_render')
                )
                results.append({
                    'template_name': request['template_name'],
                    'status': 'success',
                    'rendered_subject': result.get('subject'),
                    'body_preview': result.get('body', '')[:100] + '...' if result.get('body') else ''
                })
            except Exception as e:
                results.append({
                    'template_name': request['template_name'],
                    'status': 'error',
                    'error': str(e)
                })

        logger.info(
            f"Bulk render completed: {len([r for r in results if r['status'] == 'success'])} successful, {len([r for r in results if r['status'] == 'error'])} failed")

        return {
            'status': 'completed',
            'total_requests': len(render_requests),
            'successful': len([r for r in results if r['status'] == 'success']),
            'failed': len([r for r in results if r['status'] == 'error']),
            'results': results
        }

    except Exception as e:
        logger.error(f"Bulk render task failed: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }


@shared_task
def update_template_cache_for_template(template_id):
    """Update cache for a specific template."""
    try:
        template = NotificationTemplate.objects.get(
            id=template_id, is_active=True)

        # Clear existing cache
        TemplateService.clear_template_cache(
            template.name, template.language, template.template_type
        )

        # Warm cache
        TemplateService.get_template(
            template.name, template.language, template.template_type
        )

        logger.info(f"Updated cache for template: {template.name}")
        return {
            'status': 'success',
            'template_name': template.name,
            'language': template.language,
            'template_type': template.template_type
        }

    except NotificationTemplate.DoesNotExist:
        logger.warning(f"Template not found for cache update: {template_id}")
        return {
            'status': 'error',
            'error': 'Template not found'
        }
    except Exception as e:
        logger.error(
            f"Error updating template cache for {template_id}: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }
