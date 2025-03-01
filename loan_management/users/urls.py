from django.urls import path,include
from . views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('otp/', VerifyOTPView.as_view(), name='otp'),
    path('login/', LoginView.as_view(), name='login'),


    path("ad/loans/", AdminLoanListView.as_view(), name="admin-loan-list"),  # List all loans
    path("ad/loans/<str:loan_id>/", AdminLoanDetailView.as_view(), name="admin-loan-detail"),  # View loan details
    path("ad/loans/<str:loan_id>/delete/", AdminLoanDeleteView.as_view(), name="admin-loan-delete"),  # Delete loan

     
]
