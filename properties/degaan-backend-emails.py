from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_lead_notification_email(lead):
    """Send notification email to admin when new lead is created"""
    subject = f"New Lead: {lead.name} - {lead.get_interest_type_display()}"

    context = {
        'lead': lead,
        'interest_type': lead.get_interest_type_display(),
        'status': lead.get_status_display(),
    }

    # Email to admin
    admin_message = f"""
New Lead Received:

Name: {lead.name}
Email: {lead.email}
Phone: {lead.phone}
Interest: {lead.get_interest_type_display()}
Message: {lead.message}

Status: New
Created: {lead.created_date}

Login to dashboard to view full details:
{settings.SITE_URL}/admin/leads/lead/{lead.id}/change/
    """

    send_mail(
        subject,
        admin_message,
        settings.DEFAULT_FROM_EMAIL,
        ['info@degaanrealestate.com'],
        fail_silently=True,
    )

    # Confirmation email to lead
    lead_subject = "We received your inquiry - Degaan Real Estate"
    lead_message = f"""
Dear {lead.name},

Thank you for reaching out to Degaan Real Estate. We have received your inquiry about {lead.get_interest_type_display()}.

Our team will review your request and contact you within 24 hours.

Best regards,
Degaan Real Estate Team
+252 638 888 250
info@degaanrealestate.com
    """

    send_mail(
        lead_subject,
        lead_message,
        settings.DEFAULT_FROM_EMAIL,
        [lead.email],
        fail_silently=True,
    )


def send_property_inquiry_email(lead, property_obj):
    """Send email when lead inquires about specific property"""
    subject = f"Property Inquiry: {property_obj.address}"

    message = f"""
New property inquiry from {lead.name}

Property: {property_obj.address}
Price: ${property_obj.price:,.2f}
Size: {property_obj.size} sqft
Bedrooms: {property_obj.bedrooms}

Interested Party:
Name: {lead.name}
Email: {lead.email}
Phone: {lead.phone}

Contact them to provide more details about the property.
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['info@degaanrealestate.com'],
        fail_silently=True,
    )
