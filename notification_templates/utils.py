import logging
import re
from typing import Any, Dict

from django.template import Context, Engine, Template
from django.template.exceptions import TemplateSyntaxError

logger = logging.getLogger(__name__)


class TemplateRenderer:
    """Handles template rendering with variable substitution and HTML support."""

    def __init__(self, template):
        self.template = template
        self.content = template.content

    def render(self, context: Dict[str, Any]) -> Dict[str, str]:
        """Render template with given context."""
        try:
            rendered_data = {}

            # Render subject if exists
            if self.content.subject:
                subject_template = Template(self.content.subject)
                rendered_data["subject"] = subject_template.render(Context(context))

            # Render body with HTML support
            if self.content.is_html:
                # Use Django template engine for HTML templates
                engine = Engine.get_default()
                body_template = engine.from_string(self.content.body)
                rendered_data["body"] = body_template.render(Context(context))
            else:
                # Plain text rendering
                body_template = Template(self.content.body)
                rendered_data["body"] = body_template.render(Context(context))

            # Add template metadata
            rendered_data["template_name"] = self.template.name
            rendered_data["template_type"] = self.template.template_type
            rendered_data["language"] = self.template.language
            rendered_data["version"] = self.template.version
            rendered_data["is_html"] = self.content.is_html

            return rendered_data

        except TemplateSyntaxError as e:
            logger.error(
                f"Template syntax error in {self.template.name} ({self.template.language}, {self.template.template_type}): {str(e)}"
            )
            raise ValueError(f"Template syntax error: {str(e)}")
        except Exception as e:
            logger.error(
                f"Error rendering template {self.template.name} ({self.template.language}, {self.template.template_type}): {str(e)}"
            )
            raise ValueError(f"Template rendering error: {str(e)}")

    def validate_context(self, context: Dict[str, Any]) -> bool:
        """Validate if context contains all required variables."""
        available_vars = set(self.content.extracted_variables)
        provided_vars = set(context.keys())

        missing_vars = available_vars - provided_vars
        if missing_vars:
            logger.warning(
                f"Missing variables in context for template {self.template.name} ({self.template.language}, {self.template.template_type}): {missing_vars}"
            )
            return False

        return True


class AdvancedTemplateRenderer:
    """Advanced template renderer with additional features."""

    @staticmethod
    def render_complete_email(
        template_name, context, language="en", template_type="email"
    ):
        """Render complete email with all components."""
        from .services import TemplateService

        template = TemplateService.get_template(template_name, language, template_type)
        if not template:
            raise ValueError(f"Template not found: {template_name}")

        renderer = TemplateRenderer(template)
        result = renderer.render(context)

        # Add additional email metadata
        result["complete_email"] = {
            "from_email": context.get("from_email", "noreply@company.com"),
            "to_email": context.get("to_email"),
            "subject": result["subject"],
            "body": result["body"],
            "content_type": "text/html" if template.content.is_html else "text/plain",
        }

        return result
