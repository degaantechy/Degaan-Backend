from django.conf import settings
from django.core.mail import send_mail


def send_lead_notification_email(lead):
    """Notify the office and confirm receipt to the prospective client."""
    admin_subject = (
        f'New Lead: {lead.name} - {lead.get_interest_type_display()}'
    )
    admin_message = f"""
New Lead Received:

Name: {lead.name}
Email: {lead.email}
Phone: {lead.phone}
Interest: {lead.get_interest_type_display()}
Message: {lead.message}

Status: {lead.get_status_display()}
Created: {lead.created_date}

Login to the dashboard:
{settings.SITE_URL}/admin/leads/lead/{lead.id}/change/
    """

    send_mail(
        admin_subject,
        admin_message,
        settings.DEFAULT_FROM_EMAIL,
        ['info@degaanrealestate.com'],
        fail_silently=True,
    )

    confirmation_subject = 'We received your inquiry - Degaan Real Estate'
    confirmation_message = f"""
Dear {lead.name},

Thank you for reaching out to Degaan Real Estate. We have received your
inquiry about {lead.get_interest_type_display()}.

Our team will review your request and contact you within 24 hours.

Best regards,
Degaan Real Estate Team
+252 638 888 250
info@degaanrealestate.com
    """

    send_mail(
        confirmation_subject,
        confirmation_message,
        settings.DEFAULT_FROM_EMAIL,
        [lead.email],
        fail_silently=True,
    )
