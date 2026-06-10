from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import NotificationTemplate, TemplateContent
from .services import TemplateVersionService


class TemplateVersionServiceTest(TestCase):
    def setUp(self):
        self.template = NotificationTemplate.objects.create(
            name="test_template",
            language="en",
            template_type="email",
            version=1,
            is_active=True,
        )
        TemplateContent.objects.create(
            template=self.template,
            subject="Old Subject",
            body="Old Body",
        )

    def test_create_new_version(self):
        new_subject = "New Subject"
        new_body = "New Body"
        new_description = "New Description"

        new_version = TemplateVersionService.create_new_version(
            template_name=self.template.name,
            language=self.template.language,
            template_type=self.template.template_type,
            subject=new_subject,
            body=new_body,
            description=new_description,
        )

        self.assertIsNotNone(new_version)
        self.assertEqual(new_version.version, 2)
        self.assertTrue(new_version.is_active)
        self.assertEqual(new_version.description, new_description)

        # Verify the old version is inactive
        old_version = NotificationTemplate.objects.get(version=1)
        self.assertFalse(old_version.is_active)

        # Verify the new content is correct
        new_content = TemplateContent.objects.get(template=new_version)
        self.assertEqual(new_content.subject, new_subject)
        self.assertEqual(new_content.body, new_body)

        # Test creating a version when no active template exists
        with self.assertRaises(ValueError):
            TemplateVersionService.create_new_version(
                template_name="non_existent_template",
                language="en",
                template_type="email",
                subject="subject",
                body="body",
            )


class TemplateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.template_data = {
            "name": "api_test_template",
            "language": "en",
            "template_type": "email",
            "subject": "API Test Subject",
            "body": "API Test Body",
            "description": "API Test Description",
        }

    def test_create_new_template(self):
        response = self.client.post(
            "/api/v1/templates/", self.template_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NotificationTemplate.objects.count(), 1)
        self.assertEqual(TemplateContent.objects.count(), 1)

        template = NotificationTemplate.objects.first()
        self.assertEqual(template.name, self.template_data["name"])
        self.assertEqual(template.version, 1)
        self.assertTrue(template.is_active)

    def test_create_new_version_of_existing_template(self):
        # First, create a template
        self.client.post("/api/v1/templates/",
                         self.template_data, format="json")
        self.assertEqual(NotificationTemplate.objects.count(), 1)

        # Now, create a new version
        new_version_data = self.template_data.copy()
        new_version_data["subject"] = "New Version Subject"
        new_version_data["body"] = "New Version Body"

        response = self.client.post(
            "/api/v1/templates/", new_version_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NotificationTemplate.objects.count(), 2)

        # Check that the new version is active and the old one is not
        old_version = NotificationTemplate.objects.get(version=1)
        new_version = NotificationTemplate.objects.get(version=2)

        self.assertFalse(old_version.is_active)
        self.assertTrue(new_version.is_active)
        self.assertEqual(new_version.content.subject, "New Version Subject")

    def test_rollback_template(self):
        # Create a template (version 1)
        response = self.client.post(
            "/api/v1/templates/", self.template_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        template_id = response.data['id']

        # Create a new version (version 2)
        new_version_data = self.template_data.copy()
        new_version_data["subject"] = "Version 2 Subject"
        self.client.post("/api/v1/templates/", new_version_data, format="json")

        # Create another new version (version 3)
        third_version_data = self.template_data.copy()
        third_version_data["subject"] = "Version 3 Subject"
        self.client.post("/api/v1/templates/",
                         third_version_data, format="json")

        self.assertEqual(NotificationTemplate.objects.count(), 3)

        # Rollback to version 2
        response = self.client.post(
            f"/api/v1/templates/{template_id}/rollback/", {"version": 2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        v1 = NotificationTemplate.objects.get(
            name=self.template_data['name'], version=1)
        v2 = NotificationTemplate.objects.get(
            name=self.template_data['name'], version=2)
        v3 = NotificationTemplate.objects.get(
            name=self.template_data['name'], version=3)

        self.assertFalse(v1.is_active)
        self.assertTrue(v2.is_active)
        self.assertFalse(v3.is_active)
