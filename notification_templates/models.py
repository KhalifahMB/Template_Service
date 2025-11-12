from django.db import models
import uuid
import logging
import re
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


class NotificationTemplate(models.Model):
    TEMPLATE_TYPES = [
        ("email", "Email"),
        ("push", "Push Notification"),
    ]

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    name = models.CharField(
        max_length=200,
        help_text="A unique name for the template (e.g., 'welcome_email')",
    )
    language = models.CharField(
        max_length=10,
        default="en",
        help_text="Language code for the template (e.g., 'en', 'es', 'fr')",
    )
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        default="email",
        help_text="Type of notification template",
    )
    version = models.PositiveIntegerField(
        default=1, help_text="Current version of the template"
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this template version is active"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Description of what this template is used for"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "language", "version")
        ordering = ["name", "language", "-version"]
        indexes = [
            models.Index(fields=["name", "language"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["template_type"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.language}) - v{self.version}"

    def clean(self):
        """Validate the template before saving."""
        super().clean()

        if self.language and not re.match(r"^[a-z]{2}(-[A-Z]{2})?$", self.language):
            raise ValidationError(
                {"language": 'Language code should be in format like "en" or "en-US"'}
            )

        if self.name and not re.match(r"^[a-zA-Z0-9_-]+$", self.name):
            raise ValidationError(
                {
                    "name": "Name can only contain letters, numbers, underscores, and hyphens"
                }
            )

    @classmethod
    def get_active_template(cls, name, language="en", template_type="email"):
        """Get the active template by name, language, and type."""
        try:
            return cls.objects.select_related("content").get(
                name=name,
                language=language,
                template_type=template_type,
                is_active=True,
            )
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_template_versions(cls, name, language="en"):
        """Get all versions of a template."""
        return cls.objects.filter(name=name, language=language).order_by("-version")

    def create_new_version(self, subject, body, description=None):
        """Create a new version of this template."""
        from .services import TemplateService

        # Deactivate current version
        NotificationTemplate.objects.filter(
            name=self.name,
            language=self.language,
            template_type=self.template_type,
            is_active=True,
        ).update(is_active=False)

        # Create new version
        new_version = NotificationTemplate.objects.create(
            name=self.name,
            language=self.language,
            template_type=self.template_type,
            version=self.version + 1,
            description=description or self.description,
            is_active=True,
        )

        # Create version content
        TemplateContent.objects.create(template=new_version, subject=subject, body=body)

        # Clear cache for this template
        TemplateService.clear_template_cache(
            self.name, self.language, self.template_type
        )

        logger.info(
            f"Created new version {new_version.version} for template {self.name}"
        )
        return new_version


class TemplateContent(models.Model):
    """Stores the actual content of each template version."""

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    template = models.OneToOneField(
        NotificationTemplate, on_delete=models.CASCADE, related_name="content"
    )
    subject = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Subject line of the notification (can contain variables)",
    )
    body = models.TextField(
        help_text="The main content of the notification (can contain variables)"
    )
    is_html = models.BooleanField(
        default=True, help_text="Whether the body contains HTML content"
    )
    extracted_variables = models.JSONField(
        default=list,
        blank=True,
        help_text="Automatically extracted variable names from subject and body.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Content for {self.template.name} v{self.template.version}"

    def _extract_variables_from_content(self):
        """Extracts variable names from the subject and body using a regex pattern."""
        variables = set()
        pattern = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}"

        for content in [self.subject, self.body]:
            if content:
                variables.update(re.findall(pattern, content))

        return sorted(list(variables))

    def save(self, *args, **kwargs):
        """Extract variables before saving."""
        self.extracted_variables = self._extract_variables_from_content()
        super().save(*args, **kwargs)


class TemplateRenderLog(models.Model):
    """Log template rendering for monitoring and analytics."""

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    template = models.ForeignKey(
        NotificationTemplate, on_delete=models.CASCADE, related_name="render_logs"
    )
    context_used = models.JSONField(help_text="Context variables used for rendering")
    rendered_subject = models.TextField(blank=True, null=True)
    rendered_body = models.TextField()
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)
    requested_by = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Service or user that requested the template",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["template", "created_at"]),
            models.Index(fields=["success", "created_at"]),
        ]

    def __str__(self):
        return f"Render log for {self.template.name} at {self.created_at}"
