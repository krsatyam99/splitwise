from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from .models import UserProfile, Expense, ExpenseParticipant, Balance,User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from expenses import models
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_expense_email(expense):
    subject = 'Expense Split Information'
    from_email = 'myexamplel@example.com'  
    to_email = [participant.user.email for participant in expense.participants.all()]

    # Render the email template with the expense information
    context = {'expense': expense}
    html_message = render_to_string('emailtemplate.html', context)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject,
        plain_message,
        from_email,
        to_email,
        html_message=html_message,
    )








# Create your views here.
def test(request):
    return HttpResponse('test')



class loginview(APIView):
    authentication_classes = [ BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    

class BillSplitView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        user = request.user

        if data.get('case') == 1:
            participants = data.get('participants', [])
            total_amount = float(data.get('total_amount', 0))
            
            if not participants or total_amount <= 0:
                return Response({'error': 'Invalid input for case 1'}, status=400)

            split_amount = total_amount / len(participants)

            # Create Expense
            expense = Expense.objects.create(
                name=data.get('expense_name', 'Default Expense'),
                amount=total_amount,
                creator=user
            )

            # Create ExpenseParticipants
            for participant_id in participants:
                participant = User.objects.get(id=participant_id)
                ExpenseParticipant.objects.create(
                    user=participant,
                    expense=expense,
                    share=split_amount
                )

        elif data.get('case') == 2:
            total_amount = float(data.get('total_amount', 0))

            if total_amount <= 0:
                return Response({'error': 'Invalid input for case 2'}, status=400)

            # Create Expense
            expense = Expense.objects.create(
                name=data.get('expense_name', 'Default Expense'),
                amount=total_amount,
                creator=user
            )

            # Create ExpenseParticipants with user paying the whole amount
            ExpenseParticipant.objects.create(
                user=user,
                expense=expense,
                share=total_amount
            )

        elif data.get('case') == 3:
            custom_splits = data.get('custom_splits', {})

            if not custom_splits:
                return Response({'error': 'Invalid input for case 3'}, status=400)

            # Create Expense
            expense = Expense.objects.create(
                name=data.get('expense_name', 'Default Expense'),
                amount=sum(custom_splits.values()),
                creator=user
            )

            # Create ExpenseParticipants with custom splits
            for participant_id, share_amount in custom_splits.items():
                participant = User.objects.get(id=participant_id)
                ExpenseParticipant.objects.create(
                    user=participant,
                    expense=expense,
                    share=share_amount
                )

        else:
            return Response({'error': 'Invalid case'}, status=400)

        return Response({'message': 'Bill split successfully'})







@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
@login_required
def total_amount_to_pay_api(request):
    user = request.user
    total_to_pay = ExpenseParticipant.objects.filter(user=user, paid__lt=models.F('share')) \
                      .aggregate(Sum('remaining_amount'))['remaining_amount__sum'] or 0

    return Response({'total_to_pay': total_to_pay}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
@login_required
def amount_to_pay_for_expense_api(request, expense_id):
    user = request.user
    expense_participant = get_object_or_404(ExpenseParticipant, user=user, expense_id=expense_id)
    amount_to_pay = expense_participant.remaining_amount

    return Response({'amount_to_pay': amount_to_pay}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
@login_required
def mark_expense_as_paid_api(request, expense_id):
    user = request.user
    expense = get_object_or_404(Expense, id=expense_id, creator=user)

    if request.method == 'POST':
        expense_participant = get_object_or_404(ExpenseParticipant, user=user, expense=expense)
        expense_participant.paid = True
        expense_participant.save()

        return Response({'message': 'Expense marked as paid successfully'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)