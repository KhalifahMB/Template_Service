from django.contrib import admin

from .models import NotificationTemplate, TemplateContent, TemplateRenderLog


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "language",
        "template_type",
        "version",
        "is_active",
        "created_at",
    ]
    list_filter = ["template_type", "language", "is_active", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(TemplateContent)
class TemplateContentAdmin(admin.ModelAdmin):
    list_display = ["template", "created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["id", "created_at", "extracted_variables"]


@admin.register(TemplateRenderLog)
class TemplateRenderLogAdmin(admin.ModelAdmin):
    list_display = ["template", "success", "requested_by", "created_at"]
    list_filter = ["success", "created_at"]
    search_fields = ["template__name", "requested_by"]
    readonly_fields = ["id", "created_at"]
