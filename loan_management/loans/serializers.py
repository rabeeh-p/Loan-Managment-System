from rest_framework import serializers
from decimal import Decimal
import uuid
from datetime import datetime, timedelta
from .models import *


class PaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchedule
        fields = ["installment_no", "due_date", "amount"]

class LoanSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  
    loan_id = serializers.CharField(read_only=True)   
    payment_schedule = PaymentScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = ["loan_id", "user", "amount", "tenure", "interest_rate", 
                  "monthly_installment", "total_interest", "total_amount", "payment_schedule",'status']

 

    def validate_amount(self, value):
        if value < 1000 or value > 100000:
            raise serializers.ValidationError("Loan amount must be between ₹1,000 and ₹100,000.")
        return value
    
    def validate_interest_rate(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError("Interest rate must be between 1% and 100%.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            amount = data.get("amount")

            if Loan.objects.filter(user=user, amount=amount, status="ACTIVE").exists():
                raise serializers.ValidationError(
                    {"amount": "You already have an active loan with this amount. Another loan with the same amount is not allowed."}
                )
        return data



    def calculate_emi(self, amount, tenure, interest_rate):
        r = (interest_rate / 100) / 12   
        n = tenure
        if r == 0:
            emi = amount / n
        else:
            emi = amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return round(emi, 2)

    def generate_payment_schedule(self, loan, emi, tenure):
        start_date = datetime.today()
        schedule = []
        for i in range(1, tenure + 1):
            schedule.append(PaymentSchedule(
                loan=loan,
                installment_no=i,
                due_date=(start_date + timedelta(days=30 * i)).date(),
                amount=emi
            ))
        return schedule

    def create(self, validated_data):
        request = self.context.get('request')   
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user   
        else:
            raise serializers.ValidationError("User must be authenticated to create a loan")

        amount = validated_data["amount"]
        tenure = validated_data["tenure"]
        interest_rate = validated_data["interest_rate"]

        emi = self.calculate_emi(amount, tenure, interest_rate)
        total_interest = round((emi * tenure) - amount, 2)
        total_amount = round(amount + total_interest, 2)

        loan = Loan.objects.create(
            user=validated_data["user"],   
            amount=amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_installment=emi,
            total_interest=total_interest,
            total_amount=total_amount
        )

        payment_schedules = self.generate_payment_schedule(loan, emi, tenure)
        PaymentSchedule.objects.bulk_create(payment_schedules)

        return loan





