from django.core.management.base import BaseCommand
from notification_templates.models import NotificationTemplate, TemplateContent


class Command(BaseCommand):
    help = 'Populate database with push notification templates only'

    def handle(self, *args, **options):
        push_templates = [
            # ==================== PUSH NOTIFICATION TEMPLATES ====================
            # English Push Templates
            {
                'name': 'welcome_push',
                'language': 'en',
                'template_type': 'push',
                'body': '👋 Welcome {{user_name}}! Your {{app_name}} account is ready. Tap to explore features.',
                'description': 'Welcome push notification for new users',
                'category': 'welcome'
            },
            {
                'name': 'order_confirmed',
                'language': 'en',
                'template_type': 'push',
                'body': '✅ Order confirmed! Your order #{{order_number}} is being processed. Estimated delivery: {{delivery_date}}.',
                'description': 'Order confirmation push',
                'category': 'order'
            },
            {
                'name': 'order_shipped',
                'language': 'en',
                'template_type': 'push',
                'body': '🚚 Shipped! Order #{{order_number}} is on its way. Track delivery: {{tracking_link}}',
                'description': 'Order shipped notification',
                'category': 'order'
            },
            {
                'name': 'order_delivered',
                'language': 'en',
                'template_type': 'push',
                'body': '📦 Delivered! Your order #{{order_number}} has been delivered. Rate your experience.',
                'description': 'Order delivered notification',
                'category': 'order'
            },
            {
                'name': 'security_alert',
                'language': 'en',
                'template_type': 'push',
                'body': '⚠️ Security Alert: New sign-in from {{device_type}} in {{location}}. Tap if unfamiliar.',
                'description': 'Security alert for suspicious activity',
                'category': 'security'
            },
            {
                'name': 'password_changed',
                'language': 'en',
                'template_type': 'push',
                'body': '🔐 Password updated successfully. If you didn\'t make this change, secure your account immediately.',
                'description': 'Password change confirmation',
                'category': 'security'
            },
            {
                'name': 'promo_limited_time',
                'language': 'en',
                'template_type': 'push',
                'body': '🎁 Limited time! Get {{discount_amount}} off with code {{promo_code}}. Ends {{expiry_time}}!',
                'description': 'Limited time promotional offer',
                'category': 'promotional'
            },
            {
                'name': 'flash_sale',
                'language': 'en',
                'template_type': 'push',
                'body': '⚡ Flash Sale! {{discount_percent}}% off selected items. Only {{time_remaining}} left!',
                'description': 'Flash sale notification',
                'category': 'promotional'
            },
            {
                'name': 'abandoned_cart',
                'language': 'en',
                'template_type': 'push',
                'body': '🛒 Forgot something? Your cart with {{item_count}} items is waiting. Complete your purchase now!',
                'description': 'Abandoned cart reminder',
                'category': 'reminder'
            },
            {
                'name': 'appointment_reminder',
                'language': 'en',
                'template_type': 'push',
                'body': '📅 Reminder: Appointment with {{professional_name}} in {{time_until_appointment}}. Location: {{location}}.',
                'description': 'Appointment reminder',
                'category': 'reminder'
            },
            {
                'name': 'payment_success',
                'language': 'en',
                'template_type': 'push',
                'body': '💳 Payment successful! ${{amount}} charged for {{service_name}}. Receipt: {{receipt_link}}',
                'description': 'Payment success notification',
                'category': 'transaction'
            },
            {
                'name': 'refund_processed',
                'language': 'en',
                'template_type': 'push',
                'body': '💰 Refund processed! ${{amount}} has been refunded to your account. Should arrive in {{processing_time}}.',
                'description': 'Refund processed notification',
                'category': 'transaction'
            },
            {
                'name': 'friend_activity',
                'language': 'en',
                'template_type': 'push',
                'body': '👥 {{friend_name}} just {{activity}}! Join them and see what\'s happening.',
                'description': 'Friend activity notification',
                'category': 'social'
            },
            {
                'name': 'new_message',
                'language': 'en',
                'template_type': 'push',
                'body': '💬 New message from {{sender_name}}: "{{message_preview}}..."',
                'description': 'New message notification',
                'category': 'communication'
            },
            {
                'name': 'system_maintenance',
                'language': 'en',
                'template_type': 'push',
                'body': '🛠️ Scheduled maintenance: {{service_name}} will be unavailable from {{start_time}} to {{end_time}}.',
                'description': 'System maintenance notification',
                'category': 'system'
            },
            {
                'name': 'feature_update',
                'language': 'en',
                'template_type': 'push',
                'body': '🎉 New feature alert! {{feature_name}} is now available. Tap to learn more and try it out!',
                'description': 'New feature announcement',
                'category': 'update'
            },

            # French Push Templates
            {
                'name': 'welcome_push',
                'language': 'fr',
                'template_type': 'push',
                'body': '👋 Bienvenue {{user_name}} ! Votre compte {{app_name}} est prêt. Appuyez pour explorer les fonctionnalités.',
                'description': 'Notification push de bienvenue',
                'category': 'welcome'
            },
            {
                'name': 'order_confirmed',
                'language': 'fr',
                'template_type': 'push',
                'body': '✅ Commande confirmée ! Votre commande #{{order_number}} est en cours de traitement. Livraison estimée : {{delivery_date}}.',
                'description': 'Confirmation de commande push',
                'category': 'order'
            },
            {
                'name': 'order_shipped',
                'language': 'fr',
                'template_type': 'push',
                'body': '🚚 Expédiée ! La commande #{{order_number}} est en route. Suivre la livraison : {{tracking_link}}',
                'description': 'Notification d\'expédition',
                'category': 'order'
            },
            {
                'name': 'order_delivered',
                'language': 'fr',
                'template_type': 'push',
                'body': '📦 Livrée ! Votre commande #{{order_number}} a été livrée. Évaluez votre expérience.',
                'description': 'Notification de livraison',
                'category': 'order'
            },
            {
                'name': 'security_alert',
                'language': 'fr',
                'template_type': 'push',
                'body': '⚠️ Alerte de sécurité : Nouvelle connexion depuis {{device_type}} à {{location}}. Appuyez si non reconnue.',
                'description': 'Alerte de sécurité pour activité suspecte',
                'category': 'security'
            },
            {
                'name': 'password_changed',
                'language': 'fr',
                'template_type': 'push',
                'body': '🔐 Mot de passe mis à jour avec succès. Si vous n\'avez pas effectué cette modification, sécurisez votre compte immédiatement.',
                'description': 'Confirmation de changement de mot de passe',
                'category': 'security'
            },
            {
                'name': 'promo_limited_time',
                'language': 'fr',
                'template_type': 'push',
                'body': '🎁 Temps limité ! Obtenez {{discount_amount}} de réduction avec le code {{promo_code}}. Se termine {{expiry_time}} !',
                'description': 'Offre promotionnelle limitée',
                'category': 'promotional'
            },
            {
                'name': 'flash_sale',
                'language': 'fr',
                'template_type': 'push',
                'body': '⚡ Vente flash ! {{discount_percent}}% de réduction sur articles sélectionnés. Plus que {{time_remaining}} !',
                'description': 'Notification de vente flash',
                'category': 'promotional'
            },
            {
                'name': 'abandoned_cart',
                'language': 'fr',
                'template_type': 'push',
                'body': '🛒 Oublié quelque chose ? Votre panier avec {{item_count}} articles vous attend. Finalisez votre achat maintenant !',
                'description': 'Rappel de panier abandonné',
                'category': 'reminder'
            },
            {
                'name': 'appointment_reminder',
                'language': 'fr',
                'template_type': 'push',
                'body': '📅 Rappel : Rendez-vous avec {{professional_name}} dans {{time_until_appointment}}. Lieu : {{location}}.',
                'description': 'Rappel de rendez-vous',
                'category': 'reminder'
            },
            {
                'name': 'payment_success',
                'language': 'fr',
                'template_type': 'push',
                'body': '💳 Paiement réussi ! {{amount}} € facturés pour {{service_name}}. Reçu : {{receipt_link}}',
                'description': 'Notification de succès de paiement',
                'category': 'transaction'
            },
            {
                'name': 'refund_processed',
                'language': 'fr',
                'template_type': 'push',
                'body': '💰 Remboursement traité ! {{amount}} € ont été remboursés sur votre compte. Devrait arriver dans {{processing_time}}.',
                'description': 'Notification de remboursement traité',
                'category': 'transaction'
            },
            {
                'name': 'friend_activity',
                'language': 'fr',
                'template_type': 'push',
                'body': '👥 {{friend_name}} vient de {{activity}} ! Rejoignez-les et voyez ce qui se passe.',
                'description': 'Notification d\'activité d\'ami',
                'category': 'social'
            },
            {
                'name': 'new_message',
                'language': 'fr',
                'template_type': 'push',
                'body': '💬 Nouveau message de {{sender_name}} : "{{message_preview}}..."',
                'description': 'Notification de nouveau message',
                'category': 'communication'
            },
            {
                'name': 'system_maintenance',
                'language': 'fr',
                'template_type': 'push',
                'body': '🛠️ Maintenance programmée : {{service_name}} sera indisponible de {{start_time}} à {{end_time}}.',
                'description': 'Notification de maintenance système',
                'category': 'system'
            },
            {
                'name': 'feature_update',
                'language': 'fr',
                'template_type': 'push',
                'body': '🎉 Nouvelle fonctionnalité ! {{feature_name}} est maintenant disponible. Appuyez pour en savoir plus et l\'essayer !',
                'description': 'Annonce de nouvelle fonctionnalité',
                'category': 'update'
            },
        ]

        created_count = 0
        updated_count = 0

        for template_data in push_templates:
            name = template_data['name']
            language = template_data['language']
            template_type = template_data['template_type']
            body = template_data['body']
            description = template_data['description']
            category = template_data.get('category', 'general')

            # Check if active template already exists
            existing_template = NotificationTemplate.objects.filter(
                name=name,
                language=language,
                template_type=template_type,
                is_active=True
            ).first()

            if existing_template:
                # Update existing template
                existing_template.content.body = body
                existing_template.content.save()
                existing_template.description = description
                existing_template.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Updated push template: {name} ({language}) - {category}')
                )
            else:
                # Create new template
                template = NotificationTemplate.objects.create(
                    name=name,
                    language=language,
                    template_type=template_type,
                    description=description
                )

                TemplateContent.objects.create(
                    template=template,
                    subject='',  # Push notifications don't have subjects
                    body=body,
                    is_html=False  # Push notifications are plain text
                )

                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created push template: {name} ({language}) - {category}')
                )

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\nPush notification population completed!\n'
                f'• Created: {created_count} push templates\n'
                f'• Updated: {updated_count} push templates\n'
                f'• Total push templates: {NotificationTemplate.objects.filter(template_type="push").count()}'
            )
        )

        # Show push template counts by category
        import collections
        categories = collections.Counter()
        for template in push_templates:
            categories[template['category']] += 1

        self.stdout.write('\nPush template categories:')
        for category, count in categories.items():
            self.stdout.write(f'• {category.title()}: {count} templates')
