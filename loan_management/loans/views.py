from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoanSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

from decimal import Decimal





class LoanAPIView(APIView):
    authentication_classes = [JWTAuthentication]   
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user.role != "USER":
                return Response(
                    {"status": "error", "message": "Permission denied. Only users can access this data."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            loans = Loan.objects.filter(user=request.user)
            
            if not loans.exists():
                raise NotFound("No loans found for this user.")

            serializer = LoanSerializer(loans, many=True)

            response_data = {
                "status": "success",
                "data": {"loans": serializer.data}
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response(
                {"status": "error", "message": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": "Something went wrong."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


 
    def post(self, request):
        try:
            if request.user.role != "USER":
                return Response(
                    {"status": "error", "message": "Permission denied. Only users can access this data."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = LoanSerializer(
                data=request.data, context={'request': request}
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"status": "success", "data": serializer.data}, 
                    status=status.HTTP_201_CREATED
                )

            return Response(
                {"status": "error", "message": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": "Something went wrong."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    





class LoanForeclosureAPIView(APIView):
    authentication_classes = [JWTAuthentication]   
    permission_classes = [IsAuthenticated]

    
    def post(self, request, loan_id):
        try:
            if request.user.role != "USER":
                return Response(
                    {"status": "error", "message": "Permission denied. Only users can access this data."}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            loan = get_object_or_404(Loan, loan_id=loan_id, user=request.user)

            if loan.status != "ACTIVE":
                return Response(
                    {"status": "error", "message": "Loan is already closed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            foreclosure_discount = Decimal("500.00")  

            final_settlement_amount = max(Decimal("0.00"), loan.amount_remaining - foreclosure_discount)

            loan.status = "CLOSED"
            loan.save()

            response_data = {
                "status": "success",
                "message": "Loan foreclosed successfully.",
                "data": {
                    "loan_id": loan.loan_id,
                    "amount_paid": loan.amount_paid,
                    "foreclosure_discount": str(foreclosure_discount),   
                    "final_settlement_amount": str(final_settlement_amount),   
                    "status": loan.status
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Loan.DoesNotExist:
            return Response(
                {"status": "error", "message": "Loan not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )






