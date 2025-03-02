from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from django.contrib.auth import authenticate
from django.conf import settings
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from loans.models import *
from loans.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_403_FORBIDDEN,HTTP_404_NOT_FOUND,HTTP_204_NO_CONTENT

# Create your views here.




class RegisterView(APIView):
    permission_classes = [AllowAny]

  
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get("email")
                role = serializer.validated_data.get("role", "USER")   

                if role == "ADMIN":  
                    user = User.objects.create_user(**serializer.validated_data)
                    return Response(
                        {
                            "message": "Admin registered successfully.",
                            "user": UserSerializer(user).data
                        },
                        status=status.HTTP_201_CREATED
                    )

                otp = str(random.randint(100000, 999999))

                request.session[f"otp_{email}"] = {
                    "otp": otp,
                    "user_data": serializer.validated_data
                }
                request.session.set_expiry(300)  

                send_mail(
                    "Your OTP Code",
                    f"Your OTP for registration is {otp}. It is valid for 5 minutes.",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                return Response(
                    {"message": "OTP sent successfully. Please verify OTP."},
                    status=status.HTTP_200_OK
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response(
                {"status": "error", "message": "User with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": "Something went wrong.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

   

    def post(self, request):
        try:
            print("OTP verification process started.")
            entered_otp = request.data.get("otp")

            if not entered_otp:
                return Response(
                    {"error": "OTP is required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            email = None
            for key, value in request.session.items():
                if key.startswith("otp_") and value["otp"] == entered_otp:
                    email = key.replace("otp_", "")
                    break

            print("Session Data:", dict(request.session))  

            if not email:
                return Response(
                    {"error": "Invalid or expired OTP."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_data = request.session.get(f"otp_{email}")
            if not user_data:
                return Response(
                    {"error": "OTP expired."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.create_user(**user_data["user_data"])

            del request.session[f"otp_{email}"]

            return Response(
                {
                    "message": "OTP verified. User registered successfully.",
                    "user": UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )

        except IntegrityError:
            return Response(
                {"error": "User with this email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": "Something went wrong.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class LoginView(APIView):
    permission_classes = [AllowAny]

   
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response(
                    {"error": "Username and password are required."}, 
                    status=HTTP_400_BAD_REQUEST
                )

            user = authenticate(username=username, password=password)

            if user is None:
                return Response(
                    {"error": "Invalid credentials."}, 
                    status=HTTP_400_BAD_REQUEST
                )

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    },
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                },
                status=HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Something went wrong.", "details": str(e)},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )








class AdminLoanListView(APIView):
  

    def get(self, request):
        try:
            print("Loans endpoint hit.")

            if request.user.role != "ADMIN":
                return Response(
                    {"error": "Permission denied. Only admins can access this data."}, 
                    status=HTTP_403_FORBIDDEN
                )

            loans = Loan.objects.all()
            serializer = LoanSerializer(loans, many=True)

            return Response(
                {"status": "success", "data": serializer.data}, 
                status=HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "Something went wrong.", "details": str(e)}, 
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )



class AdminLoanDetailView(APIView):

    def get(self, request, loan_id):
        try:
            if request.user.role != "ADMIN":
                return Response(
                    {"error": "Permission denied. Only admins can access loan details."}, 
                    status=HTTP_403_FORBIDDEN
                )

            loan = get_object_or_404(Loan, loan_id=loan_id)
            serializer = LoanSerializer(loan)

            return Response(
                {"status": "success", "data": serializer.data}, 
                status=HTTP_200_OK
            )

        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found."}, 
                status=HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": "Something went wrong.", "details": str(e)}, 
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminLoanDeleteView(APIView):

    def delete(self, request, loan_id):
        try:
            if request.user.role != "ADMIN":
                return Response(
                    {"error": "Permission denied. Only admins can delete loans."},
                    status=HTTP_403_FORBIDDEN
                )

            loan = get_object_or_404(Loan, loan_id=loan_id)
            loan.delete()

            return Response(
                {"status": "success", "message": "Loan deleted successfully"},
                status=HTTP_200_OK  
            )

        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found."},
                status=HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": "Something went wrong.", "details": str(e)},
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )


