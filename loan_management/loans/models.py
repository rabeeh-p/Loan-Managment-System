from django.db import models
import uuid
from users.models import *
# Create your models here.


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    loan_id = models.CharField(max_length=20, unique=True, )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()   
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)   
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('ACTIVE', 'ACTIVE'), ('CLOSED', 'CLOSED')], default='ACTIVE')

    def __str__(self):
        return self.loan_id
    
    def save(self, *args, **kwargs):
        if not self.loan_id:  
            while True:
                new_loan_id = uuid.uuid4().hex[:10].upper()
                if not Loan.objects.filter(loan_id=new_loan_id).exists():
                    self.loan_id = new_loan_id
                    break
        super().save(*args, **kwargs)
    





class PaymentSchedule(models.Model):
    loan = models.ForeignKey(Loan, related_name="payment_schedule", on_delete=models.CASCADE)
    installment_no = models.IntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["installment_no"]