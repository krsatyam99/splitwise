from django.urls import path
from expenses.views import *

urlpatterns = [
    path('test/', test ),
    path('login/',loginview.as_view() ),
    path('split_bill/', BillSplitView.as_view()),
     path('total_amount_to_pay/',total_amount_to_pay_api ),
    path('amount_to_pay_for_expense/', amount_to_pay_for_expense_api),
     path('mark_expense_as_paid/',mark_expense_as_paid_api ),


   


]
   