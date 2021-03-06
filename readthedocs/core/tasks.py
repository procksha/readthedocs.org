"""Basic tasks"""

import logging

from celery import task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


log = logging.getLogger(__name__)


@task(queue='web')
def send_email_task(recipient, subject, template, template_html, context=None):
    """Send multipart email

    recipient
        Email recipient address

    subject
        Email subject header

    template
        Plain text template to send

    template_html
        HTML template to send as new message part

    context
        A dictionary to pass into the template calls
    """
    msg = EmailMultiAlternatives(
        subject,
        get_template(template).render(context),
        settings.DEFAULT_FROM_EMAIL,
        [recipient]
    )
    msg.attach_alternative(get_template(template_html).render(context),
                           'text/html')
    msg.send()
    log.info('Sent email to recipient: %s', recipient)
