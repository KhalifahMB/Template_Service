from django.core.management.base import BaseCommand

from notification_templates.models import NotificationTemplate, TemplateContent


class Command(BaseCommand):
    help = "Populate database with sample HTML templates in English and French"

    def handle(self, *args, **options):
        templates_data = [
            # English Templates
            {
                "name": "welcome_email",
                "language": "en",
                "template_type": "email",
                "subject": "Welcome to Our Platform, {{user_name}}!",
                "body": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 12px; }
        .highlight { background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome Aboard!</h1>
        </div>
        <div class="content">
            <h2>Hello {{user_name}},</h2>
            <p>We're thrilled to welcome you to <strong>{{company_name}}</strong>! Your account has been successfully created and you're now part of our growing community.</p>

            <div class="highlight">
                <p><strong>Your temporary password:</strong> {{temp_password}}</p>
                <p><strong>Account created on:</strong> {{signup_date}}</p>
            </div>

            <p>To get started, please click the button below to set up your account:</p>
            <center>
                <a href="{{setup_link}}" class="button">Complete Your Setup</a>
            </center>

            <p>If you have any questions, don't hesitate to contact our support team at {{support_email}}.</p>

            <p>Best regards,<br>The {{company_name}} Team</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 {{company_name}}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
                """.strip(),
                "description": "Welcome email for new users with account setup",
            },
            {
                "name": "password_reset",
                "language": "en",
                "template_type": "email",
                "subject": "Password Reset Request for Your Account",
                "body": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color: white; padding: 25px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; border-radius: 0 0 8px 8px; }
        .button { display: inline-block; padding: 14px 28px; background: #ff6b6b; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 20px 0; }
        .footer { text-align: center; margin-top: 30px; color: #777; font-size: 12px; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 6px; margin: 20px 0; }
        .code { font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Password Reset</h1>
        </div>
        <div class="content">
            <h2>Hello {{user_name}},</h2>
            <p>We received a request to reset your password for your account at <strong>{{company_name}}</strong>.</p>

            <div class="warning">
                <p><strong>Important:</strong> This password reset link will expire in <strong>{{expiry_hours}} hours</strong>.</p>
            </div>

            <p>Click the button below to create a new password:</p>
            <center>
                <a href="{{reset_link}}" class="button">Reset Your Password</a>
            </center>

            <p>Or copy and paste this link in your browser:</p>
            <div class="code">{{reset_link}}</div>

            <p>If you didn't request this password reset, please ignore this email or contact our support team at {{support_email}} if you have concerns.</p>

            <p>Stay secure,<br>The {{company_name}} Team</p>
        </div>
        <div class="footer">
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
                """.strip(),
                "description": "Password reset email with secure link",
            },
            {
                "name": "order_confirmation",
                "language": "en",
                "template_type": "email",
                "subject": "Order Confirmation - #{{order_number}}",
                "body": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; padding: 25px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; border-radius: 0 0 8px 8px; }
        .order-details { background: #f8f9fa; padding: 20px; border-radius: 6px; margin: 20px 0; }
        .product { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e9ecef; }
        .total { font-weight: bold; font-size: 18px; color: #2c3e50; margin-top: 15px; }
        .footer { text-align: center; margin-top: 30px; color: #777; font-size: 12px; }
        .status { display: inline-block; padding: 5px 15px; background: #d4edda; color: #155724; border-radius: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Order Confirmed!</h1>
        </div>
        <div class="content">
            <h2>Thank you for your order, {{customer_name}}!</h2>
            <p>We're preparing your order and will notify you when it ships.</p>

            <div class="order-details">
                <h3>Order Details</h3>
                <p><strong>Order Number:</strong> #{{order_number}}</p>
                <p><strong>Order Date:</strong> {{order_date}}</p>
                <p><strong>Status:</strong> <span class="status">{{order_status}}</span></p>

                <h4>Items Ordered:</h4>
                {% for item in order_items %}
                <div class="product">
                    <span>{{item.name}} (Qty: {{item.quantity}})</span>
                    <span>${{item.price}}</span>
                </div>
                {% endfor %}

                <div class="total">
                    <span>Total: ${{order_total}}</span>
                </div>
            </div>

            <p><strong>Shipping Address:</strong><br>
            {{shipping_address}}</p>

            <p>You can track your order anytime by visiting <a href="{{tracking_link}}">your account</a>.</p>

            <p>If you have any questions about your order, please contact us at {{support_email}} or call {{support_phone}}.</p>

            <p>Happy shopping!<br>The {{company_name}} Team</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 {{company_name}}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
                """.strip(),
                "description": "Order confirmation email with receipt",
            },
            # French Templates
            {
                "name": "welcome_email",
                "language": "fr",
                "template_type": "email",
                "subject": "Bienvenue sur Notre Plateforme, {{user_name}} !",
                "body": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
        .button { display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
        .footer { text-align: center; margin-top: 30px; color: #666; font-size: 12px; }
        .highlight { background: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Bienvenue à Bord !</h1>
        </div>
        <div class="content">
            <h2>Bonjour {{user_name}},</h2>
            <p>Nous sommes ravis de vous accueillir sur <strong>{{company_name}}</strong> ! Votre compte a été créé avec succès et vous faites maintenant partie de notre communauté grandissante.</p>

            <div class="highlight">
                <p><strong>Votre mot de passe temporaire :</strong> {{temp_password}}</p>
                <p><strong>Compte créé le :</strong> {{signup_date}}</p>
            </div>

            <p>Pour commencer, veuillez cliquer sur le bouton ci-dessous pour configurer votre compte :</p>
            <center>
                <a href="{{setup_link}}" class="button">Compléter Votre Configuration</a>
            </center>

            <p>Si vous avez des questions, n'hésitez pas à contacter notre équipe de support à {{support_email}}.</p>

            <p>Cordialement,<br>L'Équipe {{company_name}}</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 {{company_name}}. Tous droits réservés.</p>
        </div>
    </div>
</body>
</html>
                """.strip(),
                "description": "Email de bienvenue pour les nouveaux utilisateurs",
            },
            {
                "name": "password_reset",
                "language": "fr",
                "template_type": "email",
                "subject": "Demande de Réinitialisation de Mot de Passe",
                "body": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); color: white; padding: 25px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; border-radius: 0 0 8px 8px; }
        .button { display: inline-block; padding: 14px 28px; background: #ff6b6b; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; margin: 20px 0; }
        .footer { text-align: center; margin-top: 30px; color: #777; font-size: 12px; }
        .warning { background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 6px; margin: 20px 0; }
        .code { font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Réinitialisation du Mot de Passe</h1>
        </div>
        <div class="content">
            <h2>Bonjour {{user_name}},</h2>
            <p>Nous avons reçu une demande de réinitialisation de mot de passe pour votre compte chez <strong>{{company_name}}</strong>.</p>

            <div class="warning">
                <p><strong>Important :</strong> Ce lien de réinitialisation expirera dans <strong>{{expiry_hours}} heures</strong>.</p>
            </div>

            <p>Cliquez sur le bouton ci-dessous pour créer un nouveau mot de passe :</p>
            <center>
                <a href="{{reset_link}}" class="button">Réinitialiser Votre Mot de Passe</a>
            </center>

            <p>Ou copiez et collez ce lien dans votre navigateur :</p>
            <div class="code">{{reset_link}}</div>

            <p>Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email ou contacter notre équipe de support à {{support_email}}.</p>

            <p>Restez en sécurité,<br>L'Équipe {{company_name}}</p>
        </div>
        <div class="footer">
            <p>Ceci est un message automatisé. Veuillez ne pas répondre à cet email.</p>
        </div>
    </div>
</body>
</html>
                """.strip(),
                "description": "Email de réinitialisation de mot de passe",
            },
            {
                "name": "order_confirmation",
                "language": "fr",
                "template_type": "email",
                "subject": "Confirmation de Commande - #{{order_number}}",
                "body": """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); color: white; padding: 25px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; border-radius: 0 0 8px 8px; }
        .order-details { background: #f8f9fa; padding: 20px; border-radius: 6px; margin: 20px 0; }
        .product { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e9ecef; }
        .total { font-weight: bold; font-size: 18px; color: #2c3e50; margin-top: 15px; }
        .footer { text-align: center; margin-top: 30px; color: #777; font-size: 12px; }
        .status { display: inline-block; padding: 5px 15px; background: #d4edda; color: #155724; border-radius: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Commande Confirmée !</h1>
        </div>
        <div class="content">
            <h2>Merci pour votre commande, {{customer_name}} !</h2>
            <p>Nous préparons votre commande et vous informerons dès son expédition.</p>

            <div class="order-details">
                <h3>Détails de la Commande</h3>
                <p><strong>Numéro de commande :</strong> #{{order_number}}</p>
                <p><strong>Date de commande :</strong> {{order_date}}</p>
                <p><strong>Statut :</strong> <span class="status">{{order_status}}</span></p>

                <h4>Articles commandés :</h4>
                {% for item in order_items %}
                <div class="product">
                    <span>{{item.name}} (Qté: {{item.quantity}})</span>
                    <span>{{item.price}} €</span>
                </div>
                {% endfor %}

                <div class="total">
                    <span>Total : {{order_total}} €</span>
                </div>
            </div>

            <p><strong>Adresse de livraison :</strong><br>
            {{shipping_address}}</p>

            <p>Vous pouvez suivre votre commande à tout moment en visitant <a href="{{tracking_link}}">votre compte</a>.</p>

            <p>Si vous avez des questions concernant votre commande, veuillez nous contacter à {{support_email}} ou appeler le {{support_phone}}.</p>

            <p>Bon shopping !<br>L'Équipe {{company_name}}</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 {{company_name}}. Tous droits réservés.</p>
        </div>
    </div>
</body>
</html>
                """.strip(),
                "description": "Email de confirmation de commande avec reçu",
            },
        ]

        created_count = 0
        updated_count = 0

        for template_data in templates_data:
            name = template_data.pop("name")
            language = template_data.pop("language")
            template_type = template_data.pop("template_type")
            subject = template_data.pop("subject")
            body = template_data.pop("body")
            description = template_data.pop("description")

            # Check if active template already exists
            existing_template = NotificationTemplate.objects.filter(
                name=name,
                language=language,
                template_type=template_type,
                is_active=True,
            ).first()

            if existing_template:
                # Update existing template content
                existing_template.content.subject = subject
                existing_template.content.body = body
                existing_template.content.save()
                existing_template.description = description
                existing_template.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Updated template: {name} ({language})")
                )
            else:
                # Create new template
                template = NotificationTemplate.objects.create(
                    name=name,
                    language=language,
                    template_type=template_type,
                    description=description,
                )

                TemplateContent.objects.create(
                    template=template, subject=subject, body=body, is_html=True
                )

                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created template: {name} ({language})")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated database! Created: {created_count}, Updated: {updated_count}"
            )
        )
