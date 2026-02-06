from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

def send_user_email(subject, message, recipient_list, attachment_paths=None):
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list
        )
        email.content_subtype = 'html'  # Pour envoyer un email en HTML

        if attachment_paths:
            for path in attachment_paths:
                email.attach_file(path)

        email.send(fail_silently=False)
    except Exception as e:
        import logging
        logging.error(f"Erreur lors de l'envoi de mail : {e}")

    


def send_email_to_admins(subject, message, attachment_paths=None):
    admins = User.objects.filter(is_staff=True).values_list('email', flat=True)
    if not admins:
        return
    send_user_email(subject, message, list(admins), attachment_paths or [])
    
