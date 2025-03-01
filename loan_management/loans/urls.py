from django.urls import path
from . views import *

urlpatterns = [
    path("api/loans/", LoanAPIView.as_view(), name="add-loan"),
    

     
]
