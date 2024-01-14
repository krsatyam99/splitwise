from django.contrib import admin
from expenses.models import *

# Register your models here.
class user_admin(admin.ModelAdmin):
    list_display=('id','user','userId','email','mobile_number','net_balance')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'creator','amount')

    def get_participants(self, obj):
        # Retrieve related participants and join their usernames
        return ", ".join([participant.username for participant in obj.participants.all()])

    get_participants.short_description = 'Participants'

admin.site.register(Expense, ExpenseAdmin)



admin.site.register(UserProfile,user_admin)

# class Expenseparticipants(admin.ModelAdmin):
#     list_display=('id','user','share','paid')
# admin.site.register(ExpenseParticipant,Expenseparticipants)

class ExpenseParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'share', 'paid','utr_no', 'expense','get_expense_creator')

    def get_expense_creator(self, obj):
        return obj.expense.creator.username

    get_expense_creator.short_description = 'Expense Creator'

admin.site.register(ExpenseParticipant, ExpenseParticipantAdmin)


admin.site.register(Balance)
