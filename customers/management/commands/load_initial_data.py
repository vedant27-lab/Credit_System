import pandas as pd
from django.core.management.base import BaseCommand
from customers.models import Customer
from loans.models import Loan
from django.db import transaction


class Command(BaseCommand):
    help = "Load initial customer and loan data from Excel files"
    @transaction.atomic
    def handle(self, *args, **kwargs):
        customer_df = pd.read_excel("customer_data.xlsx")
        for _, row in customer_df.iterrows():
            Customer.objects.update_or_create(
                customer_id=row["Customer ID"],
                defaults={
                    "first_name": row["First Name"],
                    "last_name": row["Last Name"],
                    "age": row["Age"],
                    "phone_number": str(row["Phone Number"]),
                    "monthly_salary": row["Monthly Salary"],
                    "approved_limit": row["Approved Limit"],
                }
            )
        self.stdout.write(self.style.SUCCESS("Customers loaded successfully."))
        loan_df = pd.read_excel("loan_data.xlsx")
        for _, row in loan_df.iterrows():
            try:
                customer = Customer.objects.get(
                    customer_id=row["Customer ID"]
                )
            except Customer.DoesNotExist:
                continue
            Loan.objects.update_or_create(
                loan_id=row["Loan ID"],
                defaults={
                    "customer": customer,
                    "loan_amount": row["Loan Amount"],
                    "tenure": row["Tenure"],
                    "interest_rate": row["Interest Rate"],
                    "monthly_payment": row["Monthly payment"],
                    "emis_paid_on_time": row["EMIs paid on Time"],
                    "date_of_approval": row["Date of Approval"],
                    "end_date": row["End Date"],
                }
            )
        self.stdout.write(self.style.SUCCESS("Loans loaded successfully."))
