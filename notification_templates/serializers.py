from rest_framework import serializers

from .models import NotificationTemplate, TemplateContent, TemplateRenderLog


class TemplateContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateContent
        fields = ["id", "subject", "body", "extracted_variables", "created_at"]
        read_only_fields = ["id", "extracted_variables", "created_at"]


class NotificationTemplateSerializer(serializers.ModelSerializer):
    content = TemplateContentSerializer(read_only=True)

    class Meta:
        model = NotificationTemplate
        fields = [
            "id",
            "name",
            "language",
            "template_type",
            "version",
            "is_active",
            "description",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "version", "created_at", "updated_at"]


class TemplateCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    language = serializers.CharField(max_length=10, default="en")
    template_type = serializers.ChoiceField(
        choices=NotificationTemplate.TEMPLATE_TYPES, default="email"
    )
    subject = serializers.CharField(max_length=255, required=False, allow_blank=True)
    body = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_name(self, value):
        import re

        if not re.match(r"^[a-zA-Z0-9_-]+$", value):
            raise serializers.ValidationError(
                "Name can only contain letters, numbers, underscores, and hyphens"
            )
        return value

    def validate_language(self, value):
        import re

        if value and not re.match(r"^[a-z]{2}(-[A-Z]{2})?$", value):
            raise serializers.ValidationError(
                'Language code should be in format like "en" or "en-US"'
            )
        return value


class TemplateUpdateSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255, required=False, allow_blank=True)
    body = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)


class TemplateRenderSerializer(serializers.Serializer):
    template_name = serializers.CharField(max_length=200)
    language = serializers.CharField(max_length=10, default="en")
    template_type = serializers.ChoiceField(
        choices=NotificationTemplate.TEMPLATE_TYPES, default="email"
    )
    context = serializers.JSONField()
    requested_by = serializers.CharField(max_length=100, required=False)


class TemplateRenderResponseSerializer(serializers.Serializer):
    subject = serializers.CharField(allow_null=True)
    body = serializers.CharField()
    template_name = serializers.CharField()
    template_type = serializers.CharField()
    language = serializers.CharField()
    version = serializers.IntegerField()


class TemplateRenderLogSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source="template.name", read_only=True)

    class Meta:
        model = TemplateRenderLog
        fields = [
            "id",
            "template_name",
            "context_used",
            "rendered_subject",
            "rendered_body",
            "success",
            "error_message",
            "requested_by",
            "created_at",
        ]
        read_only_fields = fields


class CompleteTemplateRenderSerializer(serializers.Serializer):
    template_name = serializers.CharField(max_length=200)
    language = serializers.CharField(max_length=10, default="en")
    template_type = serializers.ChoiceField(
        choices=NotificationTemplate.TEMPLATE_TYPES, default="email"
    )
    context = serializers.JSONField()
    requested_by = serializers.CharField(max_length=100, required=False)


class CompleteTemplateRenderResponseSerializer(serializers.Serializer):
    subject = serializers.CharField(allow_null=True)
    body = serializers.CharField()
    template_name = serializers.CharField()
    template_type = serializers.CharField()
    language = serializers.CharField()
    version = serializers.IntegerField()
    is_html = serializers.BooleanField()
    complete_email = serializers.DictField()
