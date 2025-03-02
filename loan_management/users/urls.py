from django.urls import path,include
from . views import *

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/otp/', VerifyOTPView.as_view(), name='otp'),
    path('api/login/', LoginView.as_view(), name='login'),


    path("api/admin/loans/", AdminLoanListView.as_view(), name="admin-loan-list"),  
    path("api/admin/loans/<str:loan_id>/", AdminLoanDetailView.as_view(), name="admin-loan-detail"),  
    path("api/admin/loans/<str:loan_id>/delete/", AdminLoanDeleteView.as_view(), name="admin-loan-delete"),  

     
]
