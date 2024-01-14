from django.urls import path
from expenses.views import *

urlpatterns = [
    path('test/', test ),
    path('login/',loginview.as_view() ),
    path('split_bill/', BillSplitView.as_view()),

   


]
   