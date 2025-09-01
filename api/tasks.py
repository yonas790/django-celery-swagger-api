from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_email_notification(self, subject, message, recipient_list):
    """
    Send email notification as a background task
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
        return f"Email sent to {recipient_list}"
    except Exception as exc:
        logger.error(f"Email sending failed: {exc}")
        # Retry the task
        raise self.retry(exc=exc, countdown=60)

@shared_task
def send_daily_report():
    """
    Send daily report - example periodic task
    """
    try:
        # Daily report logic here
        subject = "Daily Report"
        message = "This is your daily report."
        recipient_list = ["abebe@gmail.com"]
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        logger.info("Daily report sent successfully")
        return "Daily report sent"
    except Exception as exc:
        logger.error(f"Daily report failed: {exc}")
        raise exc

@shared_task
def process_data_task(data):
    """
    Example data processing task
    """
    try:
        # Simulate data processing
        import time
        time.sleep(5)  # Simulate processing time
        
        logger.info(f"Processed data: {data}")
        return f"Processed: {data}"
    except Exception as exc:
        logger.error(f"Data processing failed: {exc}")
        raise exc
