
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import timedelta
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def send_expense_email_task(expense_id):
    from models import Expense  
    try:
        expense = Expense.objects.get(id=expense_id)

        subject = 'Expense Split Information'
        from_email = 'example@example.com'  # enter your mail.
        to_email = [participant.user.email for participant in expense.participants.all()]

        # Render the email template with the expense information
        context = {'expense': expense}
        html_message = render_to_string('expense_email_template.html', context)
        plain_message = strip_tags(html_message)

        # Send the email
        send_mail(
            subject,
            plain_message,
            from_email,
            to_email,
            html_message=html_message,
        )

        logger.info(f"Expense email sent successfully for expense ID {expense_id}")

    except Expense.DoesNotExist:
        logger.error(f"Expense with ID {expense_id} does not exist.")
