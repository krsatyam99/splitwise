from django.db import models
import uuid
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userId = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    net_balance=models.DecimalField(max_digits=12, decimal_places=2,default=1000,null=True)

class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses')
    participants = models.ManyToManyField(User, through='ExpenseParticipant')

class ExpenseParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)
    utr_no = models.CharField(null=True, max_length=30)

class Balance(models.Model):
    debtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debts')
    creditor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    @classmethod
    def update_balances(cls, expense):
        participants = expense.participants.all()
        total_share = sum(expense_participant.share for expense_participant in expense.expenseparticipant_set.all())
        for participant in participants:
            share_paid = expense.expenseparticipant_set.get(user=participant).paid
            balance, created = cls.objects.get_or_create(debtor=participant, creditor=expense.creator)
            balance.amount += share_paid - total_share / len(participants)
            balance.save()
