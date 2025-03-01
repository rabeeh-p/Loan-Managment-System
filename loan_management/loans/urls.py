from django.urls import path
from .views import *

urlpatterns = [
    path("api/loans/", LoanAPIView.as_view(), name="add-loan"),
    path('api/loans/<str:loan_id>/foreclose/',LoanForeclosureAPIView.as_view(), name='loan-foreclosure'),
    

     
]
